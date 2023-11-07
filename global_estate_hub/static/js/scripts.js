/**
   * HEADER USER DROPDOWN
    */

const $userDropdown = document.querySelector('[data-user-dropdown]')

if($userDropdown){
  const $dropDownToggler = $userDropdown.querySelector('[data-show-user-nav]')
  const $userNav = $userDropdown.querySelector('[data-user-dropdown-nav]')
  $dropDownToggler.addEventListener('click', ()=> {
    if ( !$userNav.classList.contains('active') ) {
      $userNav.classList.add('active')

      window.addEventListener('click', (e)=>{
        if( e.target !== $dropDownToggler && !$dropDownToggler.contains(e.target) ){
          $userNav.classList.remove('active')
        }
      })
    } else{
      $userNav.classList.remove('active')
    }
  })
}


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
            $messageNode.classList.add('success')
            $messageNode.classList.remove('error')
            $emailInput.value = ""
            setTimeout(() => {
              $messageNode.remove()
            }, "3000");
          } else{
            $messageNode.classList.add('error')
            $messageNode.classList.remove('success')
          }
          $messageNode.textContent = response.message
      }
    }
  })
}


/**
   * FORMS
    */

const $eyeIcons = document.querySelectorAll('[data-password-eye]')

if($eyeIcons.length){
  $eyeIcons.forEach(eye => {
    const $input = eye.parentElement.querySelector('input')
    eye.addEventListener('click', ()=>{
      if ( $input.type === 'password' ){
        $input.type = 'text'
      } else{
        $input.type = 'password'
      }
    })
  });
}


const userFormsValidation = ($form, response, redirectionPath) => {
  const fieldsNumber = response.length
  let validFields = 0

  response.forEach(field => {
    const $currentformField = $form.querySelector(`[${field.field}]`).closest('.form__field')
    const $message = $currentformField.querySelector('.info')
    if (field.valid == false) {
      const $message = $currentformField.querySelector('.info')
      validFields = 0

      if($message){ 
        $message.textContent = field.message 
      }else {
        const info = document.createElement('span')
        info.classList.add('info')
        info.classList.add('error')
        info.textContent = field.message
        $currentformField.append(info)
      }
    } else{
      validFields++
      if($message){ 
        $message.remove()
      }
    }

    if ( validFields === fieldsNumber ) {
      window.location.href = redirectionPath
    }
  });

}


/**
   * LOGIN FORM AJAX VALIDATION
    */

const $loginForm = document.querySelector('[data-login-form]')

if ($loginForm){
  $loginForm.addEventListener('submit', function (e) {
    e.preventDefault()
    let csrftoken = this.querySelector('[name="csrftoken"]').value
    const $emailInput = this.querySelector('[data-email]')
    const $passwordInput = this.querySelector('[data-password]')
    const $termsInput = this.querySelector('[data-terms]')

    const data = {
      "email": [$emailInput.value, "data-email"],
      "password": [$passwordInput.value, "data-password"],
      "terms": [$termsInput.checked, "data-terms"]
    }

    const xhr = new XMLHttpRequest()
    xhr.open('POST', 'login', true)
    xhr.setRequestHeader('X-CSRFToken', csrftoken)
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    xhr.send(JSON.stringify(data))

    xhr.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
          const response = JSON.parse(this.responseText)
          userFormsValidation($loginForm, response, '/')
      }
    }
  })
}


/**
   * SIGNUP FORM AJAX VALIDATION
    */

const $signUpForm = document.querySelector('[data-signup-form]')

if ($signUpForm){
  $signUpForm.addEventListener('submit', function (e) {
    e.preventDefault()
    let csrftoken = this.querySelector('[name="csrftoken"]').value
    const $userNameInput = this.querySelector('[data-username]')
    const $emailInput = this.querySelector('[data-email]')
    const $password1Input = this.querySelector('[data-password1]')
    const $password2Input = this.querySelector('[data-password2]')

    const data = {
      "userName": [$userNameInput.value, "data-username"],
      "email": [$emailInput.value, "data-email"],
      "password1": [$password1Input.value, "data-password1"],
      "password2": [$password2Input.value, "data-password2"]
    }

    const xhr = new XMLHttpRequest()
    xhr.open('POST', 'create-user', true)
    xhr.setRequestHeader('X-CSRFToken', csrftoken)
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    xhr.send(JSON.stringify(data))

    xhr.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
          const response = JSON.parse(this.responseText)
          userFormsValidation($signUpForm, response, '/login')
      }
    }
  })
}


/**
   * FORGOT PASSWORD AJAX VALIDATION
    */

const $forgotPasswordForm = document.querySelector('[data-forgot-password-form]')

if ($forgotPasswordForm){
  $forgotPasswordForm.addEventListener('submit', function (e) {
    e.preventDefault()
    let csrftoken = this.querySelector('[name="csrftoken"]').value
    const $emailInput = this.querySelector('[data-email]')

    const data = {
      "email": $emailInput.value
    }

    const xhr = new XMLHttpRequest()
    xhr.open('POST', 'forget-password', true)
    xhr.setRequestHeader('X-CSRFToken', csrftoken)
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    xhr.send(JSON.stringify(data))

    xhr.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
          const response = JSON.parse(this.responseText)
          console.log(response)

          if( response.valid == true ) {
            window.location.href = '/password-reset.html'
          } else{
            alert(response.message)
          }
      }
    }
  })
}