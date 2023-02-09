import React, {useState}  from "react";
import {Helmet} from "react-helmet";

function App() {

  
  const [light, setlight] = useState(false);

  const onCheck = () =>{
    setlight(!light);
  }


  return (
    <div class={(light)?("bg-light"):("bg-dark")}>
      <Helmet>
        <title>Minecraft: The Best Thing</title>
        <meta name="description" content="What is the best Minecraft thing to ever exist? Vote on this website, and find out which is better."></meta>
        <meta name="author" content="EPIC DEV TEAM LET'S GO"></meta>
        <meta name="keywords" content="minecraft best thing mc tom scott dukky vote dream" />
      </Helmet>
      <div class={(light)?(""):("overlay")}>
      <div class="container-fluid">
          <div class="row">
            <div class="center adj">
              <input id="toggletheme" onClick={onCheck} type="image" src={(light)?("https://i.imgur.com/rvXYKZ9.png"):("https://i.imgur.com/OWXmoUk.png")} alt="toggle theme"></input>
            </div>
		        <div class="center adj">
              <img class="title" alt="THE BEST THING" src="https://i.imgur.com/lHRDVRv.png"/>
	  	      </div>
            <div class="center adj">
              <a target="_blank" rel="noopener noreferrer" href="https://youtu.be/Y6uToji2bkg"><img id="YT" alt="YouTube video" src="https://www.freepnglogos.com/uploads/youtube-play-red-logo-png-transparent-background-6.png"/></a>
            </div>
	        </div>
          
	      <div class="row">
        <p class={(light)?("txt-light"):("txt-dark")}>The expirement has ended! Check back soon for results.</p>
          <a href="https://github.com/KyngK/bestmcthing"><p class={(light)?("txt-light"):("txt-dark")}>GitHub page</p></a>
	      </div>
      </div>
      </div>
    </div>
  );
}

export default App;
