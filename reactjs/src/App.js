import React, {useState, useEffect}  from "react";
import {Helmet} from "react-helmet";

function App() {

  const baseData = [
    {
      id:"",
      title:"",
      summary:"",
      image:null,
      url:""
    },
    {
      id:"",
      title:"",
      summary:"",
      image:null,
      url:""
    }
  ]
  const populateBaseData = () =>{
    baseData[0].image = data[0].image;
    baseData[1].image = data[1].image;
  }
  var [disabled, setDisabled] = useState(true);
  var [data, setData] = useState(baseData)
  const [light, setlight] = useState(false);

  useEffect(() => {
    fetch("/ba24d209-064f-41a9-bffc-f5050a574e16").then(
      resp => resp.json()  
    ).then(
      data => {
        setData(data)
        console.log(data)
        
      }
    ).then(setDisabled(false))
  }, [])

  const delay = ms => new Promise(res => setTimeout(res, ms));

  const toggleDisable = async () => {
    await delay(500);
    setDisabled(false);
  }

  const onCheck = () =>{
    setlight(!light);
  }

  const vote = (id0, id1, skip) =>{
    setDisabled(true);
    populateBaseData();
    setData(baseData);
    fetch("/ba24d209-064f-41a9-bffc-f5050a574e16?0=".concat(id0, "&1=", id1, (skip)?("&skip"):("")))
    .then(
      resp => resp.json()  
    ).then(
      data => {
        setData(data)
        console.log(data)
      }
    ).then(toggleDisable())
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
              <input class="toggletheme" onClick={onCheck} type="image" src={(light)?("https://i.imgur.com/rvXYKZ9.png"):("https://i.imgur.com/OWXmoUk.png")} alt="toggle theme"></input>
            </div>
		        <div class="center adj">
              <img class="title" alt="THE BEST THING" src="https://i.imgur.com/lHRDVRv.png"/>
  			      <div class="page-header">
	  			      <p style={{fontSize: '16pt'}} class={(light)?("txt-light"):("txt-dark")}>
		  			      Which is better?
			  	      </p>
  			      </div>
	  	      </div>
	        </div>
          
	      <div class="row">
          <div class="center col-md-5">
            <div class="img">
            <a target="_blank" rel="noopener noreferrer" href={data[0].url}><img alt={data[0].title} src={(data[0].image == null)? "https://i.imgur.com/OzRR1xv.jpg" : data[0].image} class="thing" /></a>
            </div>
            <button type="button" disabled={disabled} onClick={() => vote(data[1].id, data[0].id, false)}>
              {data[0].title}
            </button>
            <p style={{fontSize: '16pt'}} class={(light)?("txt-light"):("txt-dark")}>
            {(data[0].summary==="")?(<><br></br><br></br><br></br></>):(data[0].summary)}
            </p>
		      </div>
          <div class="vcenter center col-md-2">
            <img class="vs" alt="Versus" src="https://i.imgur.com/wyZeuQn.png" />
          </div>
          <div class="center col-md-5">
          <div class="img">
            <a target="_blank" rel="noopener noreferrer" href={data[1].url}><img alt={data[1].title} src={(data[1].image == null)? "https://i.imgur.com/OzRR1xv.jpg" : data[1].image} class="thing"/></a>
          </div>
            <button disabled={disabled} type="button" onClick={() => vote(data[0].id, data[1].id, false)}>
              {data[1].title}
            </button>
            <p style={{fontSize: '16pt'}} class={(light)?("txt-light"):("txt-dark")}>
              {(data[1].summary==="")?(<><br></br><br></br><br></br></>):(data[1].summary)}
            </p>
		      </div>
	      </div>
	    <div class="row">
		    <div class="center col-md-12">
			    <button disabled={disabled} type="button" onClick={() => vote(data[0].id, data[1].id, true)}>
				    Skip
			    </button>
		    </div>
	    </div>
      </div>
      </div>
    </div>
  );
}

export default App;
