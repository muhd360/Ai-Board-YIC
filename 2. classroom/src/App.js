import "./App.css";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import Home from "./screens/Home";
import Dashboard from "./screens/Dashboard";
import Navbar from "./components/Navbar";
import Class from "./screens/Class";
import Resources from "./screens/Resources";
import ResourcePage from "./screens/resourcescomponent/ResourcePage";

function App() {
  return (
    <div className="app">
      <Router>
        <Switch>
          <Route exact path="/">
            <Home />
          </Route>
          <Route exact path="/resources">
            <Resources/>
          </Route>
          <Route exact path="/resources/:lectureNumber">
            <ResourcePage/>
          </Route>
          <Route exact path="/dashboard">
            <Navbar />
            <Dashboard />
          </Route>
          <Route exact path="/class/:id">
            <Navbar />
            <Class />
          </Route>
        </Switch>
      </Router>
    </div>
  );
}

export default App;
