const xhr = new XMLHttpRequest()
const url = '/data.json'
xhr.open("GET", url)
xhr.send()

xhr.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200) {
    console.log(xhr.responseText)
  }
}