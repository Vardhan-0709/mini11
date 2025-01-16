import os
from flask import Flask, request, jsonify
import cv2
import numpy as np
import open3d as o3d

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_files():
    files = request.files.getlist("images")
    if not files or len(files) < 2:
        return jsonify({"error": "Please upload at least two images of the component"}), 400

    # Save uploaded files
    file_paths = []
    for file in files:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        file_paths.append(file_path)

    # Perform 3D reconstruction and generate views
    try:
        views = generate_views(file_paths)
        return jsonify({"views": views})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def generate_views(image_paths):
    # Placeholder 3D reconstruction logic
    # Use Structure-from-Motion (SfM) techniques or Open3D pipelines to generate the 3D model
    print("Performing 3D reconstruction...")

    # Load sample 3D model for demo
    # Replace this with your own reconstruction logic
    mesh = o3d.geometry.TriangleMesh.create_sphere(radius=1.0)  # Example model
    mesh.compute_vertex_normals()

    views = {}
    directions = {
        "top": [0, 1, 0],
        "bottom": [0, -1, 0],
        "front": [0, 0, 1],
        "back": [0, 0, -1],
        "left": [-1, 0, 0],
        "right": [1, 0, 0],
    }

    for view_name, direction in directions.items():
        vis = o3d.visualization.Visualizer()
        vis.create_window(visible=False)
        vis.add_geometry(mesh)

        ctr = vis.get_view_control()
        ctr.set_front(direction)
        ctr.set_up([0, 0, 1])
        ctr.set_lookat(mesh.get_center())
        ctr.set_zoom(0.7)

        vis.poll_events()
        vis.update_renderer()

        output_file = os.path.join(UPLOAD_FOLDER, f"{view_name}.png")
        vis.capture_screen_image(output_file)
        vis.destroy_window()

        views[view_name] = f"/static/{view_name}.png"  # Serve files from the static folder

    return views


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
