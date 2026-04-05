import React, { useState, useEffect } from 'react';
import Plot from 'react-plotly.js';
import axios from 'axios';

function App() {
  const [data, setData] = useState(null);
  const [params, setParams] = useState({ kernel: 'rbf', C: 1.0 });

  const fetchData = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/api/v1/visualize/svm/`, {
        params: params
      });
      setData(response.data);
    } catch (error) {
      console.error("Error al traer datos de ML", error);
    }
  };

  useEffect(() => { fetchData(); }, [params]);

  if (!data) return <div>Cargando motor de ML...</div>;

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>ML Decision Boundary (SVM)</h1>
      
      <div style={{ marginBottom: '20px' }}>
        <label>Kernel: </label>
        <select value={params.kernel} onChange={e => setParams({...params, kernel: e.target.value})}>
          <option value="rbf">RBF (Radial)</option>
          <option value="linear">Linear</option>
          <option value="poly">Polinomial</option>
        </select>

        <label style={{ marginLeft: '15px' }}>Regularización (C): </label>
        <input 
          type="number" 
          value={params.C} 
          step="0.1" 
          onChange={e => setParams({...params, C: e.target.value})} 
        />
      </div>

      <Plot
        data={[
          {
            z: data.grid.z,
            type: 'contour',
            colorscale: 'RdBu',
            opacity: 0.5,
            showscale: false
          },
          {
            x: data.points.x,
            y: data.points.y,
            mode: 'markers',
            type: 'scatter',
            marker: {
              color: data.points.labels,
              colorscale: 'Viridis',
              size: 10,
              line: { color: 'white', width: 1 }
            }
          }
        ]}
        layout={{ width: 800, height: 600, title: `SVM con Kernel: ${params.kernel}` }}
      />
    </div>
  );
}

export default App;