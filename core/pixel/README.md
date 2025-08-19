# 🎨 PixelPaper

A digital drawing and note-taking application integrated into the Automation Suite dashboard.

## ✨ Features

- **Drawing Tools**: Various brushes, colors, and sizes for freehand drawing
- **Note-taking**: Add text to your drawings with customizable fonts and colors
- **Layers**: Work with multiple layers for complex compositions
- **Export**: Save your artwork in various formats (PNG, JPG, PDF)
- **Undo/Redo**: Easily correct mistakes with unlimited undo/redo
- **Responsive**: Works on both desktop and tablet devices

## 🚀 Launching PixelPaper

You can launch PixelPaper in two ways:

1. **From the Dashboard**:
   - Navigate to the "Projects" section in the sidebar
   - Click on the "🎨 PixelPaper" button

2. **Directly via Command Line**:
   ```bash
   streamlit run core/pixel/PixelPaper.py
   ```

## 🛠️ Requirements

- Python 3.8+
- Streamlit
- Pillow (PIL Fork)
- Numpy

## 📝 Usage

1. **Drawing**:
   - Select a brush type and size from the toolbar
   - Choose a color from the color picker
   - Click and drag on the canvas to draw

2. **Adding Text**:
   - Click the "Add Text" button
   - Click on the canvas where you want to add text
   - Type your text in the input field that appears
   - Use the text formatting options to customize appearance

3. **Layers**:
   - Add new layers using the "+ Layer" button
   - Toggle layer visibility with the eye icon
   - Reorder layers by dragging them
   - Delete layers with the trash can icon

4. **Saving Your Work**:
   - Click the "Save" button in the toolbar
   - Choose your preferred format (PNG, JPG, or PDF)
   - Your file will be downloaded automatically

## 🔧 Customization

You can customize PixelPaper by modifying the following in `PixelPaper.py`:

- Default brush sizes and colors
- Canvas size and background
- Available fonts and text styles
- Keyboard shortcuts

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
