import React, { useState, useEffect } from 'react';
import Navbar from '../layout/Navbar';


function AccuracyReport() {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/accuracy_report')
      .then(response => response.json())
      .then(data => {
        setReport(data);
        setLoading(false);
      })
      .catch(error => console.error(error));
  }, []);

  return (
    <div style={{backgroundColor:"White",
    backgroundRepeat: "no-repeat", backgroundSize:"100%"}}>
        <Navbar/>
      {loading ? <p>Loading...</p> : report && (
        <div style={{ height: "88.95svh", color:"blue" }}>
          <h1><b>Accuracy Report</b></h1>
          <h4>Accuracy: {report.accuracy}</h4>
          <h4>Loss: {report.loss}</h4>
          <h4>Validation accuracy: {report.val_accuracy}</h4>
          <h4>Validation loss: {report.val_loss}</h4>
          <div
            style={{
              position: "absolute", // Position the images absolutely
              bottom: 8, // Place the images at the bottom of the container
              display: "flex", // Display the images in a row
              justifyContent: "center", // Center the images horizontally
              width: "100%", // Set the width of the container to 100%
            }}
          >
            <img src="/images/test.png" alt="Test" />
            <img src="/images/training_accuracy.png" alt="TrainingAccuracy" />
            <img src="/images/training_loss.png" alt="TrainingLoss" />
          </div>
        </div>
      )}
    </div>
  );
}

export default AccuracyReport;