function App() {
    const currDate = new Date();
    return (
        <div>
            <h1>Ryan Burmeister</h1>
            <h2>The date is {currDate.toLocaleDateString()}.</h2>
            <h2>The time is {currDate.toLocaleTimeString()}.</h2>
        </div>
    );
}

export default App;