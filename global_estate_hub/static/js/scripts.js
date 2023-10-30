/**
   * OFFCANVAS TOGGLE
    */

const $offcanvasToggler = document.querySelector('[data-open-offcanvas]'),
      $offcanvasWrapper = document.querySelector('[data-offcanvas]'),
      $offcanvasClose = document.querySelector('[data-close-offcanvas]')

if ( $offcanvasToggler &&  $offcanvasWrapper && $offcanvasClose ){
  $offcanvasToggler.addEventListener('click', ()=> {
    $offcanvasWrapper.classList.add('active')
  })

  $offcanvasClose.addEventListener('click', ()=> {
    $offcanvasWrapper.classList.remove('active')
  })
}



















// const form = document.querySelector('form')

// form.addEventListener('submit', e => {
//   e.preventDefault()
//   const inputValue = form.querySelector('input').value

//   const xhr = new XMLHttpRequest()
//   const url = "/add-category"
//   xhr.open("POST", url)
//   xhr.send(inputValue)

//   xhr.onreadystatechange = function () {
//     if (this.readyState == 4 && this.status == 200) {
//         console.log(xhr.responseText)
//     }
//   }
// })