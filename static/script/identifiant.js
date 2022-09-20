function identifiant_article(id){
    fetch('/article/'+id)
    .then(function (response) {
      return response.text();
    }).then(function (text) {
      //console.log(text);
      document.getElementById("lien-article").innerHTML = text;
    })
  }