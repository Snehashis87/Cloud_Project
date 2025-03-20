import { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [filter, setFilter] = useState("pencil");
  const [imageURL, setImageURL] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleFilterChange = (e) => {
    setFilter(e.target.value);
  };

  const applyFilter = async () => {
    if (!file) {
      alert("Please select an image");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("filter", filter);

    try {
      const response = await fetch("http://localhost:5000/apply-filter", {
        method: "POST",
        body: formData, // No need for Content-Type, FormData handles it
      });

      if (!response.ok) {
        throw new Error("Failed to apply filter");
      }

      const imageBlob = await response.blob();
      const imageURL = URL.createObjectURL(imageBlob);
      setImageURL(imageURL);
    } catch (error) {
      console.error("Error:", error);
      alert("Failed to connect to the server");
    }
  };

  return (
    <div>
      <h2>AI Image Filter</h2>
      <input type="file" onChange={handleFileChange} />
      <select onChange={handleFilterChange} value={filter}>
        <option value="pencil">Pencil Sketch</option>
        <option value="cartoon">Cartoon</option>
        <option value="edge">Edge Detection</option>
        <option value="grayscale">Grayscale</option>
        <option value="sepia">Sepia</option>
        <option value="invert">Invert Colors</option>
      </select>
      <button onClick={applyFilter}>Apply Filter</button>

      {imageURL && <img src={imageURL} alt="Filtered Result" />}
    </div>
  );
}

export default App;
