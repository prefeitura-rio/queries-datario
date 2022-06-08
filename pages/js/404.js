var particles = {
  fpsLimit: 60,
  particles: {
    number: {
      value: 160,
      density: {
        enable: true,
        area: 800
      }
    },
    color: {
      value: "#ffffff"
    },
    shape: {
      type: "circle"
    },
    opacity: {
      value: 1,
      random: {
        enable: true,
        minimumValue: 0.1
      },
      animation: {
        enable: true,
        speed: 1,
        minimumValue: 0,
        sync: false
      }
    },
    size: {
      value: 3,
      random: {
        enable: true,
        minimumValue: 1
      }
    },
    move: {
      enable: true,
      speed: 0.17,
      direction: "none",
      random: true,
      straight: false,
      outModes: {
        default: "out"
      }
    }
  },
  interactivity: {
    detectsOn: "canvas",
    events: {
      resize: false
    }
  },
  detectRetina: true
};

tsParticles.load("tsparticles", particles);

function getQueryParameters() {
  var queryParameters = {};
  var queryString = window.location.search.substring(1);
  var regex = /([^&=]+)=([^&]*)/g;
  var m;
  while ((m = regex.exec(queryString))) {
    queryParameters[decodeURIComponent(m[1])] = decodeURIComponent(m[2]);
  }
  // If we have queryParameters["prefix"], set the URL.
  if (queryParameters["prefix"]) {
    document.getElementById(
      "btnAcessarDado"
    ).href = `https://www.data.rio/documents/${queryParameters[
      "prefix"
    ]}/about`;
  } else {
    document.getElementById("btnAcessarDado").href = "#";
  }
}
