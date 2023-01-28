import React, {useState, useEffect}  from "react";



function App() {


  var [data, setData] = useState([{}])
  const [light, setlight] = React.useState(false);

  useEffect(() => {
    fetch("/api").then(
      resp => resp.json()  
    ).then(
      data => {
        setData(data)
        console.log(data)
      }
    )
  }, [])

  const onCheck = () =>{
    setlight(!light);
  }

  const vote = (id0, id1, skip) =>{
    fetch("/api?0=".concat(id0, "&1=", id1, (skip)?("&skip"):("")))
    .then(
      resp => resp.json()  
    ).then(
      data => {
        setData(data)
        console.log(data)
      }
    )
  }


  return (
    <div class={(light)?("bg-light"):("bg-dark")}>
      <div class={(light)?(""):("overlay")}>
	    {(data[1] === undefined) ?
        (<h1>Loading</h1>)
        :
        (<div class="container-fluid">
          <div class="row">
          <div class="col-md-2">
            <input class="toggletheme" onClick={onCheck} type="image" src={(light)?("https://i.imgur.com/rvXYKZ9.png"):("https://i.imgur.com/OWXmoUk.png")} alt="toggle theme"></input>
            </div>
		      <div class="center col-md-8">
            <img class="title" alt="THE BEST THING" src="https://i.imgur.com/lHRDVRv.png"/>
			      <div class="page-header">
				      <h3 class={(light)?("txt-light"):("txt-dark")}>
					      Which is better?
				      </h3>
  			    </div>
	  	    </div>
          <div class="col-md-2">
            </div>
	      </div>
	      <div class="row">
          <div class="center col-md-5">
            <div class="img">
            <a target="_blank" rel="noopener noreferrer" href={data[0].url}><img alt={data[0].title} src={(data[0].image == null)? "https://i.imgur.com/OzRR1xv.jpg" : data[0].image.slice(0, -35)} class="thing" /></a>
            </div>
            <button type="button" onClick={() => vote(data[1].id, data[0].id, false)}>
              {data[0].title}
            </button>
            <h3 class={(light)?("txt-light"):("txt-dark")}>
              {data[0].summary}
            </h3>
		      </div>
          <div class="vcenter center col-md-2">
            <img alt="Versus" src="https://upload.wikimedia.org/wikipedia/commons/7/70/Street_Fighter_VS_logo.png" />
          </div>
          <div class="center col-md-5">
            <a target="_blank" rel="noopener noreferrer" href={data[1].url}><img alt={data[1].title} src={(data[1].image == null)? "https://i.imgur.com/OzRR1xv.jpg" : data[1].image.slice(0, -35)} class="thing"/></a>
            <button type="button" onClick={() => vote(data[0].id, data[1].id, false)}>
              {data[1].title}
            </button>
            <h3 class={(light)?("txt-light"):("txt-dark")}>
              {data[1].summary}
            </h3>
		      </div>
	      </div>
	    <div class="row">
		    <div class="center col-md-12">
			    <button type="button" onClick={() => vote(data[0].id, data[1].id, true)}>
				    Skip
			    </button>
		    </div>
	    </div>
      </div>)}
      </div>
    </div>
  );
}

export default App;
