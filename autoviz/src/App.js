import logo from './logo.svg';
import './App.css';
import FileExplorer from './FileExplorer'
import Main from './Components/Main/Main'
import Footer from './Components/Footer/Footer'
import NavBar from './Components/NavBar/Navbar';


function App() {
  return (
    <div className="App">
      <NavBar></NavBar>
      <Main></Main>
      <Footer />
      {/* <header className="App-header">
      <FileExplorer/>
      </header>
      <main>

      </main> */}
    </div>
  );
}

export default App;
