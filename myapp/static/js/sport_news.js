var myHeaders = new Headers();
myHeaders.append("x-rapidapi-key", "0304c43f05msh6c69f0df2b39183p1b067fjsn902b7105573f");
myHeaders.append("x-rapidapi-host", "v3.football.api-sports.io");

var requestOptions = {
  method: 'GET',
  headers: myHeaders,
  redirect: 'follow'
};

fetch("https://v3.football.api-sports.io/{endpoint}", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));