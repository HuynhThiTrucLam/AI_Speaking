from flask import Blueprint, request, jsonify
from flask.views import MethodView
import os
import tempfile

from utils.audio_utils import format_audio
from services.cloudinary_service import CloudinaryUploader


audio_bp = Blueprint('audio', __name__)


class Audio(MethodView):
    def post(self):
        if 'file' not in request.files:
            return jsonify({"error": "Missing 'file' in form-data"}), 400

        file_storage = request.files['file']
        if file_storage.filename == '':
            return jsonify({"error": "Empty filename"}), 400

        # Save incoming file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False) as tmp_in:
            file_storage.save(tmp_in.name)
            input_path = tmp_in.name

        # Read optional conversion parameters
        desired_format = (request.form.get('typeWantToConvert') or 'mp3').lower()
        provided_output_path = request.form.get('outputPath')
        target_sr_str = request.form.get('targetSr')

        # Validate desired format (basic)
        if desired_format not in {'mp3', 'wav', 'flac', 'ogg', 'm4a'}:
            return jsonify({"error": f"Unsupported format: {desired_format}"}), 400

        # Resolve output path
        output_dir = tempfile.mkdtemp()
        if provided_output_path:
            # If a name only is provided, put it in temp dir; if it has an extension, keep it
            base_name = os.path.basename(provided_output_path)
            if not os.path.splitext(base_name)[1]:
                base_name = f"{base_name}.{desired_format}"
            output_path = os.path.join(output_dir, base_name)
        else:
            output_path = os.path.join(output_dir, f"converted.{desired_format}")

        # Parse target sample rate
        try:
            target_sr = int(target_sr_str) if target_sr_str else 16000
            if target_sr <= 0:
                raise ValueError
        except ValueError:
            return jsonify({"error": "Invalid targetSr; must be positive integer"}), 400
        try:
            format_audio(input_path, output_path, output_format=desired_format, mono=True, target_sr=target_sr)
        except Exception as e:
            return jsonify({"error": f"Audio conversion failed: {str(e)}"}), 500

        # Upload to Cloudinary (resource_type "video" covers audio)
        try:
            uploader = CloudinaryUploader()
            folder_param = request.form.get('folder') or 'AISpeaker'
            public_url = uploader.upload_file(output_path, folder=folder_param, resource_type='video')
        except Exception as e:
            return jsonify({"error": f"Upload failed: {str(e)}"}), 502

        return jsonify({"url": public_url})


audio_bp.add_url_rule('/audio', view_func=Audio.as_view('audio'))




