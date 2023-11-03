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

if ($newsletterForm){
  $newsletterForm.addEventListener('submit', e =>{
    e.preventDefault()
    let csrftoken = $newsletterForm.querySelector('[name="csrftoken"]').value
    const $emailInput = $newsletterForm.querySelector('[data-email]')
    const data = {
      "email": $emailInput.value
    }

    const xhr = new XMLHttpRequest()
    

    xhr.open('POST', 'newsletter', true)
    xhr.setRequestHeader('X-CSRFToken', csrftoken)
    // xhr.setRequestHeader("Content-type", "application/json")
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    xhr.send(JSON.stringify(data))

    xhr.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
          const response = JSON.parse(this.responseText)
          const info = document.createElement('span')
          info.classList.add('info')

          let $messageNode = $newsletterForm.querySelector('.info')
          if ( !$messageNode ){ 
            $newsletterForm.append(info) 
          }
          $messageNode = $newsletterForm.querySelector('.info')
          if (response.valid){
            $messageNode.classList.add('succes')
            $messageNode.classList.remove('error')
            $emailInput.value = ""
            setTimeout(() => {
              $messageNode.remove()
            }, "3000");
          } else{
            $messageNode.classList.add('error')
            $messageNode.classList.remove('succes')
          }
          $messageNode.textContent = response.message
      }
    }
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