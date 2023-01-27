import React, {useState, useEffect}  from "react";

function App() {


  var [data, setData] = useState([{}])

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
    <div>
	    {(data[1] === undefined) ?
        (<h1>Loading</h1>)
        :
        (<div class="container-fluid">
          <div class="row">
		      <div class="center col-md-12">
			      <div class="page-header">
				      <h1>
					      Which is better??
				      </h1>
  			    </div>
	  	    </div>
	      </div>
	      <div class="row">
          <div class="center col-md-5">
            <div class="img">
            <a href={data[0].url}><img alt={data[0].title} src={(data[0].image == null)? "/assets/pack.jpeg" : data[0].image.slice(0, -35)} class="thing" /></a>
            </div>
            <button type="button" onClick={() => vote(data[1].id, data[0].id, false)}>
              {data[0].title}
            </button>
            <h3>
              {data[0].summary}
            </h3>
		      </div>
          <div class="vcenter col-md-2">
            <img alt="Versus" src="https://upload.wikimedia.org/wikipedia/commons/7/70/Street_Fighter_VS_logo.png" />
          </div>
          <div class="center col-md-5">
            <a href={data[1].url}><img alt={data[1].title} src={(data[1].image == null)? "/assets/pack.jpeg" : data[1].image.slice(0, -35)} class="thing"/></a>
            <button type="button" onClick={() => vote(data[0].id, data[1].id, false)}>
              {data[1].title}
            </button>
            <h3>
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
  );
}

export default App;
