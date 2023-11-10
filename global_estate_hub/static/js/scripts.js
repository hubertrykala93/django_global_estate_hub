/*----------------------------------*\
  #HEADER
\*----------------------------------*/

/**
   * User dropdown
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
   * Offcanvas toggle
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


/*----------------------------------*\
  #HOME PAGE AND ABOUT
\*----------------------------------*/

/**
   * Testimonials carousel
    */

$testimonialsSection = document.querySelector('[data-testimonials]')

if($testimonialsSection) {
  const $testimonialsCarousel = $testimonialsSection.querySelector('[data-testimonials-carousel]')

  const swiper = new Swiper($testimonialsCarousel, {
    navigation: {
      nextEl:  $testimonialsSection.querySelector('[data-right]'),
      prevEl: $testimonialsSection.querySelector('[data-left]'),
    },
    draggable: true,
    speed: 400,
    slidesPerView: 1,
    spaceBetween: 24,
    breakpoints: {
      768: {
        slidesPerView: 2,
      },
      992: {
        slidesPerView: 3,
      }
    },
  })
}

/**
   * Our team carousel
    */

$outTeamSection = document.querySelector('[data-out-team]')

if($outTeamSection) {
  const $ourTeamCarousel = $outTeamSection.querySelector('[data-our-team-carousel]')

  const swiper = new Swiper($ourTeamCarousel, {
    navigation: {
      nextEl:  $outTeamSection.querySelector('[data-right]'),
      prevEl: $outTeamSection.querySelector('[data-left]'),
    },
    draggable: true,
    speed: 400,
    slidesPerView: 1,
    spaceBetween: 24,
    breakpoints: {
      768: {
        slidesPerView: 2,
      },
      992: {
        slidesPerView: 2,
      },
      1500: {
        slidesPerView: 3,
      },
    },
  })
}


/**
   * Our partners carousel
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


/*----------------------------------*\
  #FORMS
\*----------------------------------*/

/**
   * Newsletter footer form
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
   * Show / hide password
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

/**
   * Sign up / login validation (F)
    */
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
   * Login form ajax validation
    */

const $loginForm = document.querySelector('[data-login-form]')

if ($loginForm){
  $loginForm.addEventListener('submit', function (e) {
    e.preventDefault()
    let csrftoken = this.querySelector('[name="csrftoken"]').value
    const $emailInput = this.querySelector('[data-email]')
    const $passwordInput = this.querySelector('[data-password]')

    const data = {
      "email": [$emailInput.value, "data-email"],
      "password": [$passwordInput.value, "data-password"]
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
   * Signup form ajax validation
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
    const $termsInput = this.querySelector('[data-terms]')

    const data = {
      "userName": [$userNameInput.value, "data-username"],
      "email": [$emailInput.value, "data-email"],
      "password1": [$password1Input.value, "data-password1"],
      "password2": [$password2Input.value, "data-password2"],
      "terms": [$termsInput.checked, "data-terms"]
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
   * Forgot password ajax validation
    */

const $forgotPasswordWrapper = document.querySelector('[data-forgot-password-wrapper]')

if ($forgotPasswordWrapper){

  //2nd step
  const secondStep = ()=> {
    const $verificationForm = $forgotPasswordWrapper.querySelector('[data-verification-password-form]')
    const $verificationFormInputs = $verificationForm.querySelectorAll('[data-code]')

    $verificationFormInputs.forEach((input, index) => {
      input.addEventListener('input', ()=>{
        if ( !input.value.match(/^[0-9]+$/) ) {
          input.value = ''
          input.classList.remove('highlighted')
        } else {
          input.classList.add('highlighted')
          const inputToFocus = index + 1 < $verificationFormInputs.length ? index + 1 : false
          if (inputToFocus) { $verificationFormInputs[inputToFocus].focus() }
        }
      })
    })





  }

  //1st step
  const $forgotPasswordForm = $forgotPasswordWrapper.querySelector('[data-forgot-password-form]')

  const firstStepValidation = (form, response) =>{
    const $formField = form.querySelector('.form__field')
    const $message = $formField.querySelector('.info')

    if($message){ 
      $message.textContent = response.message 
    } else {
      const info = document.createElement('span')
      info.classList.add('info')
      info.classList.add('error')
      info.textContent = response.message
      $formField.append(info)
    }
  }

  const goToStepTwo = ()=> {
    const $stepOne = $forgotPasswordWrapper.querySelector('[data-forgot-password-step]')
    const $stepTwo = $forgotPasswordWrapper.querySelector('[data-verification-password-step]')
    $stepTwo.style.zIndex = 2
    $stepTwo.style.transform = "translateX(0)"
    

    setTimeout(() => {
      $stepOne.style.position = "absolute"
      $stepTwo.style.position = "relative"
    }, 400);

    secondStep()
  }

  $forgotPasswordForm.addEventListener('submit', function (e) {
    e.preventDefault()
    let csrftoken = this.querySelector('[name="csrftoken"]').value
    const $emailInput = this.querySelector('[data-email]')

    const data = {
      "email": $emailInput.value
    }

    const xhr = new XMLHttpRequest()
    xhr.open('POST', 'send-otp', true)
    xhr.setRequestHeader('X-CSRFToken', csrftoken)
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    xhr.send(JSON.stringify(data))

    xhr.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
          const response = JSON.parse(this.responseText)

          if( response.valid == true ) {
            goToStepTwo()
          } else{
           firstStepValidation($forgotPasswordForm, response)
          }
      }
    }
  })
}








/*----------------------------------*\
  #OTHERS
\*----------------------------------*/

/**
   * Theme accordion
    */

const $accordion = document.querySelector('[data-theme-accordion]')

if ($accordion){

  $accordion.addEventListener('click', e =>{

    function assignClickedHeading () {
      if ( e.target.hasAttribute('data-heading') ) { return e.target }
      else if ( e.target.closest('[data-heading]') ) { return e.target.closest('[data-heading]') }
      else { return false }
    }

    let $clickedHeading = assignClickedHeading()

    if ( $clickedHeading ) {
      const $allHeadings = $accordion.querySelectorAll('[data-heading]')
      const $allContents = $accordion.querySelectorAll('.accordion__content')
      const $content = $clickedHeading.nextElementSibling

      const hideContent = (content) =>{
        content.style.maxHeight = content.scrollHeight
        setTimeout(() => {
          content.style.maxHeight = '0px'
        }, 1);
      }

      if ( $clickedHeading.classList.contains('active') ) { 
        $clickedHeading.classList.remove('active')
        hideContent($content)
      } else {
        $allContents.forEach(content => {
          if ( content.previousElementSibling.classList.contains('active') ) {
            hideContent(content)
          }
        })
        $allHeadings.forEach(heading => {heading.classList.remove('active')})
        $clickedHeading.classList.add('active')
        const contentHeight = $content.scrollHeight
        $content.style.maxHeight = contentHeight + 'px'
        setTimeout(() => {
          $content.style.maxHeight = 'unset'
        }, 400);
      }
    }
  })
}