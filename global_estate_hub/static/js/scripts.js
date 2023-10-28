const form = document.querySelector('form')

form.addEventListener('submit', e => {
  e.preventDefault()
  const inputValue = form.querySelector('input').value

  const xhr = new XMLHttpRequest()
  const url = "{% url 'index' %}"
  xhr.open("POST", url)
  xhr.send(inputValue)

  xhr.onreadystatechange = function () {
    if ( this.readyState == 4 && this.status == 200) {
      console.log(xhr.responseText)
    }
  }
})