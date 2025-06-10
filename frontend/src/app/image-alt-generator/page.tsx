"use client";

import React, { useState, useCallback } from "react";
import { Upload, Image as ImageIcon, Edit, Trash2 } from "lucide-react";
import { 
  uploadImage, 
  getImages, 
  updateImageAltText, 
  deleteImage,
  ImageUploadResponse,
  ImageListResponse 
} from "@/lib/api/api-client";

export default function ImageAltGeneratorPage() {
  const [images, setImages] = useState<ImageUploadResponse[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [editingImage, setEditingImage] = useState<ImageUploadResponse | null>(null);
  const [editAltText, setEditAltText] = useState("");
  const [showEditDialog, setShowEditDialog] = useState(false);

  const showToast = (title: string, description: string, variant: "default" | "destructive" = "default") => {
    console.log(`${variant === "destructive" ? "ERROR" : "SUCCESS"}: ${title} - ${description}`);
  };

  const loadImages = useCallback(async () => {
    setIsLoading(true);
    try {
      const data = await getImages();
      setImages(data.images);
    } catch (error) {
      showToast("Error", "Failed to load images", "destructive");
    } finally {
      setIsLoading(false);
    }
  }, []);

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (!files || files.length === 0) return;

    const file = files[0];
    
    if (!file.type.startsWith("image/")) {
      showToast("Error", "Please select an image file", "destructive");
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      showToast("Error", "File size must be less than 10MB", "destructive");
      return;
    }

    setIsUploading(true);
    
    try {
      const newImage = await uploadImage(file);
      setImages(prev => [newImage, ...prev]);
      
      showToast("Success", "Image uploaded and alt text generated successfully");
      
      event.target.value = "";
    } catch (error) {
      showToast("Error", error instanceof Error ? error.message : "Upload failed", "destructive");
    } finally {
      setIsUploading(false);
    }
  };

  const handleEditAltText = (image: ImageUploadResponse) => {
    setEditingImage(image);
    setEditAltText(image.alt_text || "");
    setShowEditDialog(true);
  };

  const handleSaveAltText = async () => {
    if (!editingImage) return;

    try {
      const updatedImage = await updateImageAltText(editingImage.id, editAltText);
      setImages(prev => 
        prev.map(img => img.id === updatedImage.id ? updatedImage : img)
      );
      
      showToast("Success", "Alt text updated successfully");
      
      setEditingImage(null);
      setEditAltText("");
      setShowEditDialog(false);
    } catch (error) {
      showToast("Error", "Failed to update alt text", "destructive");
    }
  };

  const handleDeleteImage = async (imageId: number) => {
    try {
      await deleteImage(imageId);
      setImages(prev => prev.filter(img => img.id !== imageId));
      
      showToast("Success", "Image deleted successfully");
    } catch (error) {
      showToast("Error", "Failed to delete image", "destructive");
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  };

  React.useEffect(() => {
    loadImages();
  }, [loadImages]);

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">SEO Alt Text Generator</h1>
        <p className="text-gray-600">
          Upload images and generate SEO-optimized alt text using AI
        </p>
      </div>

      <div className="grid gap-6">
        <div className="bg-white rounded-lg border shadow-sm">
          <div className="p-6 border-b">
            <h2 className="text-xl font-semibold flex items-center gap-2">
              <Upload className="h-5 w-5" />
              Upload Image
            </h2>
            <p className="text-gray-600 mt-1">
              Upload an image to automatically generate SEO-optimized alt text
            </p>
          </div>
          <div className="p-6">
            <div className="space-y-4">
              <div>
                <label htmlFor="image-upload" className="block text-sm font-medium mb-1">
                  Select Image
                </label>
                <input
                  id="image-upload"
                  type="file"
                  accept="image/*"
                  onChange={handleFileUpload}
                  disabled={isUploading}
                  className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                />
                <p className="text-sm text-gray-500 mt-1">
                  Supported formats: JPEG, PNG, GIF, WebP (max 10MB)
                </p>
              </div>
              
              {isUploading && (
                <div className="flex items-center gap-2 text-sm text-gray-600">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                  Uploading and generating alt text...
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg border shadow-sm">
          <div className="p-6 border-b">
            <h2 className="text-xl font-semibold flex items-center gap-2">
              <ImageIcon className="h-5 w-5" />
              Uploaded Images
            </h2>
            <p className="text-gray-600 mt-1">
              Manage your uploaded images and their alt text
            </p>
          </div>
          <div className="p-6">
            <div className="space-y-4">
              <button 
                onClick={loadImages} 
                disabled={isLoading}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
              >
                {isLoading ? "Loading..." : "Refresh Images"}
              </button>
              
              {images.length === 0 ? (
                <div className="text-center py-8 text-gray-500">
                  No images uploaded yet. Upload your first image above.
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Image</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Original Name</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Alt Text</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Size</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {images.map((image) => (
                        <tr key={image.id}>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <img
                              src={`/api/images/${image.id}/file`}
                              alt={image.alt_text || "Uploaded image"}
                              className="w-16 h-16 object-cover rounded"
                            />
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap font-medium text-gray-900">
                            {image.original_name}
                          </td>
                          <td className="px-6 py-4 max-w-xs">
                            <div className="truncate" title={image.alt_text || ""}>
                              {image.alt_text || "No alt text"}
                            </div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className="px-2 py-1 text-xs font-medium bg-gray-100 text-gray-800 rounded">
                              {formatFileSize(image.file_size)}
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {formatDate(image.created_at)}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="flex gap-2">
                              <button
                                onClick={() => handleEditAltText(image)}
                                className="p-2 text-gray-600 hover:text-blue-600 border rounded"
                              >
                                <Edit className="h-4 w-4" />
                              </button>
                              
                              <button
                                onClick={() => handleDeleteImage(image.id)}
                                className="p-2 text-gray-600 hover:text-red-600 border rounded"
                              >
                                <Trash2 className="h-4 w-4" />
                              </button>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {showEditDialog && editingImage && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <h3 className="text-lg font-semibold mb-4">Edit Alt Text</h3>
            <p className="text-gray-600 mb-4">Update the alt text for this image</p>
            
            <div className="space-y-4">
              <div>
                <img
                  src={`/api/images/${editingImage.id}/file`}
                  alt={editingImage.alt_text || "Image preview"}
                  className="w-full max-w-sm mx-auto rounded"
                />
              </div>
              <div>
                <label htmlFor="alt-text" className="block text-sm font-medium mb-1">
                  Alt Text
                </label>
                <textarea
                  id="alt-text"
                  value={editAltText}
                  onChange={(e) => setEditAltText(e.target.value)}
                  placeholder="Enter descriptive alt text..."
                  className="w-full p-2 border rounded-md"
                  rows={3}
                />
              </div>
            </div>
            
            <div className="flex gap-2 mt-6">
              <button
                onClick={handleSaveAltText}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                Save Changes
              </button>
              <button
                onClick={() => setShowEditDialog(false)}
                className="px-4 py-2 border rounded-md hover:bg-gray-50"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
