import { useState } from 'react'
import axios from 'axios';
import './App.scss'
const App = () => {
  const parameters = ['gwl', 'pH', 'E.C', 'TDS', 'CO3', 'HCO3', 'Cl', 'F', 'NO3 ', 'SO4',
    'Na', 'K', 'Ca', 'Mg', 'T.H', 'SAR']
  
  const [isLoaded, setIsLoaded] = useState(true)
  const [isError, setIsError] = useState(false)
  // const [formData, setFormData] = useState(Array(16).fill(''))
  const [formData, setFormData] = useState([5.66, 8.02, 420, 275.3, 0.0, 153.3, 12, 0.55, 11.200, 37, 25, 1.0, 33.0, 20.5, 160.3, 0.938])
  const [prediction, setPrediction] = useState('Submit to predict the quality')
  const handleChange = (event, index) => {
    setFormData((prevData) => {
      const newData = [...prevData];
      newData[index] = event.target.value;
      return newData;
    });
  };

  const handleSubmit = (event) => {
    setIsLoaded(false)
    event.preventDefault();

    axios.post('http://localhost:8080/predict', formData, {
      headers: { 'Content-Type': 'application/json' },
    })
      .then((response) => {
        setPrediction(response.data.prediction);
        setIsLoaded(true)
        setIsError(false)// Assuming prediction is in response.data.prediction
      })
      .catch((error) => {
        setIsError(true)// Assuming prediction is in response.data.prediction
        setIsLoaded(true)
        setPrediction(error.message);
        console.error(error);
      });
  };
  return (
    <div className='main flex'>
      <form action="" className="container flex" onSubmit={handleSubmit}>
        <p class="h3">Advanced Groundwater Quality Analysis</p>
        <div className='flex inputContainer'>
          {Array(16).fill(null).map((_, index) => (
            <>
              <div className='field flex'>
                <p>{parameters[index]}</p>
                <input
                  className="form-control"
                  placeholder={parameters[index]}
                  key={index}
                  type="number" // Set type to "number" for numeric input
                  name={`input-${index + 1}`}
                  value={formData[index]}
                  onChange={(event) => handleChange(event, index)}
                  required // Mark as required
                />
              </div>
            </>
          ))}
        </div>
        <button type="submit" className="btn btn-success" disabled={formData.some((value) => value === '')}>
          Submit
        </button>
        {
          !isLoaded? <div className="spinner-border text-secondary" role="status">
          <span className="visually-hidden">Loading...</span>
          </div>
            :
        <p className={isError?"error":"noerror"}>{prediction}</p>
        }
        
      </form>
    </div>
  )
}

export default App