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


/**
   * OUR PARTNERS CAROUSEL
    */

const $partnersCarousel = document.querySelector('[data-partners-carousel]')

if($partnersCarousel){
  const swiper = new Swiper($partnersCarousel, {
    loop: true,
    draggable: true,
    speed: 400,
    spaceBetween: 30,
    autoplay: {
    delay: 1500,
    },
    slidesPerView: 2,
    breakpoints: {
      768: {
        slidesPerView: 3,
      },
      992: {
        slidesPerView: 4,
      },
      1200: {
        slidesPerView: 5,
      },
    },
  })
}


/**
   * NEWSLETTER FOOTER SUBSCRIBTION
    */

const $newsletterForm = document.querySelector('[data-newsletter-form]')
//let csrftoken = '{{ csrf_token }}'
//console.log(csrftoken)

if ($newsletterForm){
  $newsletterForm.addEventListener('submit', e =>{
    e.preventDefault()
    const dataEmail = $newsletterForm.querySelector('[data-email]').value

    const xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            console.log(JSON.parse(this.responseText))
        }
    }

    xhr.open('POST', '/newsletter')
//    xhr.setRequestHeader('X-CSRFToken', csrftoken)
    xhr.send(dataEmail)
  })











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