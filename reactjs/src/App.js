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

  return (
    <div class="container-fluid">
	    <div class="row">
		    <div class="center col-md-12">
			    <div class="page-header">
				    <h1 class="center">
					    Which is better?
				    </h1>
			    </div>
		    </div>
	    </div>
	    <div class="row">
        <div class="center col-md-5">
			    <img alt={data[0].title} src={(data[0].image == null)? "/assests/pack.jpeg" : data[0].image.slice(0, -35)} class="center" />
          <button type="button" class="center">
            {data[0].title}
          </button>
          <h3 class="center">
            {data[0].summary}
          </h3>
		    </div>
        <div class="center col-md-2">
          <h1> VS </h1>
        </div>
        <div class="center col-md-5">
			    <img alt={data[1].title} src={(data[1].image == null)? "/assests/pack.jpeg" : data[1].image.slice(0, -35)} class="center" />
          <button type="button" class="center">
            {data[1].title}
          </button>
          <h3 class="center">
            {data[1].summary}
          </h3>
		    </div>
	    </div>
	    <div class="row">
		    <div class="center col-md-12">
			    <button type="button" class="center">
				    Skip
			    </button>
		    </div>
	    </div>
    </div>
  );
}

export default App;
