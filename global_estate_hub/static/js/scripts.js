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
   * Reusable functions
    */

const getToken = (form) => {
  return form.querySelector('[name="csrftoken"]').value
}

/**
   * Newsletter footer form
    */

const $newsletterForm = document.querySelector('[data-newsletter-form]')

if ($newsletterForm){

  const showInfo = (isValid, message)=>{
    let $messageNode = $newsletterForm.querySelector('.info')
    if ( !$messageNode ){ 
      const info = document.createElement('span')
      info.classList.add('info')
      $newsletterForm.append(info) 
    }

    $messageNode = $newsletterForm.querySelector('.info')

    if ( isValid) {
      $messageNode.classList.add('success')
      $messageNode.classList.remove('error')
      $newsletterForm.querySelector('[data-email]').value = ""
      setTimeout(() => {
        $messageNode.remove()
      }, "3000");
    } else {
        $messageNode.classList.add('error')
        $messageNode.classList.remove('success')
    }
    
    $messageNode.textContent = message
  }

  const removeInfo = ()=>{
    const $messageNode = $newsletterForm.querySelector('.info')
    if ($messageNode) { $messageNode.remove() }
  }

  const serverResponse = (response) => {
    if ( response.valid === null ) {
      removeInfo()
    } else{
      showInfo(response.valid, response.message)
    }
  }

  const clientValidation = (data) => {
    const emailRegex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/

    if ( data.url !== '' ) {
      removeInfo()
    }
    else if ( data.email == '' ) {
      showInfo(false, 'The email field cannot be empty.')
    }
    else if ( !data.email.match(emailRegex) ) {
      showInfo(false, 'The e-mail address format is invalid.')
    }
    else {
      removeInfo()
      ajaxRequest(data)
    }
  }

  const ajaxRequest = (data) => {
    const xhr = new XMLHttpRequest()
    xhr.open('POST', 'newsletter', true)
    xhr.setRequestHeader('X-CSRFToken', getToken($newsletterForm))
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    xhr.send(JSON.stringify(data))

    xhr.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
          const response = JSON.parse(this.responseText)
          serverResponse(response)
      }
    }
  }

  $newsletterForm.addEventListener('submit', e =>{
    e.preventDefault()
    const $emailInput = $newsletterForm.querySelector('[data-email]')
    const $urlInput = $newsletterForm.querySelector('[name="url"]')
    const data = {
      "email": $emailInput.value.trim(),
      "url": $urlInput.value
    }
    clientValidation(data)
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

  //3rd step
  const thirdStep = ()=> {
    const $newPasswordForm = $forgotPasswordWrapper.querySelector('[data-new-password-form]')

    const goToStepFour = ()=> {
      const $stepThree = $forgotPasswordWrapper.querySelector('[data-new-password-step]')
      const $stepFour = $forgotPasswordWrapper.querySelector('[data-done-password-step]')
      $stepFour.style.zIndex = 4
      $stepFour.style.transform = "translateX(0)"
      
  
      setTimeout(() => {
        $stepThree.style.position = "absolute"
        $stepFour.style.position = "relative"
      }, 400);
    }

    const thirdStepValidation = ($form, response) => {
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
          goToStepFour()
        }
      });
    }

    $newPasswordForm.addEventListener('submit', function (e) {
      e.preventDefault()
      let csrftoken = this.querySelector('[name="csrftoken"]').value
      const $password1Input = $newPasswordForm.querySelector('[data-password1]')
      const $password2Input = $newPasswordForm.querySelector('[data-password2]')
      const data = {
        "password1": [$password1Input.value, "data-password1"],
        "password2": [$password2Input.value, "data-password2"],
        "email": sessionStorage.getItem('verifyingEmail')
      }
        
      const xhr = new XMLHttpRequest()
      xhr.open('POST', 'set-password', true)
      xhr.setRequestHeader('X-CSRFToken', csrftoken)
      xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
      xhr.send(JSON.stringify(data))
  
      xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            const response = JSON.parse(this.responseText)
            thirdStepValidation($newPasswordForm, response)
        }
      }
    })
  }

  //2nd step
  const secondStep = ()=> {
    const $verificationForm = $forgotPasswordWrapper.querySelector('[data-verification-password-form]')
    const $veryfyingEmail = $forgotPasswordWrapper.querySelector('[data-verification-email]')
    const $verificationFormInputs = $verificationForm.querySelectorAll('[data-code]')

    $veryfyingEmail.textContent = sessionStorage.getItem('verifyingEmail')

    const secondStepValidation = (form, message) =>{
      const $formField = form.querySelector('.form__field')
      const $message = $formField.querySelector('.info')
  
      if($message){ 
        $message.textContent = message 
      } else {
        const info = document.createElement('span')
        info.classList.add('info')
        info.classList.add('error')
        info.textContent = message
        $formField.append(info)
      }
    }

    const goToStepThree = ()=> {
      const $stepTwo = $forgotPasswordWrapper.querySelector('[data-verification-password-step]')
      const $stepThree = $forgotPasswordWrapper.querySelector('[data-new-password-step]')
      $stepThree.style.zIndex = 3
      $stepThree.style.transform = "translateX(0)"
      
  
      setTimeout(() => {
        $stepTwo.style.position = "absolute"
        $stepThree.style.position = "relative"
      }, 400);
  
      thirdStep()
    }

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

    $verificationForm.addEventListener('submit', function (e) {
      e.preventDefault()
      let csrftoken = this.querySelector('[name="csrftoken"]').value
      const $codeInputs = this.querySelectorAll('[data-code]')
      let filledInputs = 0
      let typedCode = ""
      $codeInputs.forEach(input=> {
        if (input.value !== ''){
          filledInputs++
          typedCode += input.value
        }
      })

      if ( filledInputs !== $codeInputs.length ) {
        secondStepValidation($verificationForm, "Fill all inputs.")
      } else {
        const data = {
          "code": typedCode,
          "email": sessionStorage.getItem('verifyingEmail')
        }
        
        const xhr = new XMLHttpRequest()
        xhr.open('POST', 'validate-password', true)
        xhr.setRequestHeader('X-CSRFToken', csrftoken)
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
        xhr.send(JSON.stringify(data))
    
        xhr.onreadystatechange = function () {
          if (this.readyState == 4 && this.status == 200) {
              const response = JSON.parse(this.responseText)
    
              if( response.valid == true ) {
                sessionStorage.setItem('verifyingEmail', response.email)
                goToStepThree()
              } else{
                secondStepValidation($verificationForm, response.message)
              }
          }
        }
      }
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
    xhr.open('POST', 'send-password', true)
    xhr.setRequestHeader('X-CSRFToken', csrftoken)
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    xhr.send(JSON.stringify(data))

    xhr.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
          const response = JSON.parse(this.responseText)

          if( response.valid == true ) {
            sessionStorage.setItem('verifyingEmail', response.email)
            goToStepTwo()
          } else{
           firstStepValidation($forgotPasswordForm, response)
          }
      }
    }
  })
}

/**
  * Contact us ajax
   */

const $contactUsForm = document.querySelector('[data-contact-form]')

if ($contactUsForm) {

  const showInfo = (isValid, message, $form, field)=> {
    const $inputParentField = $form.querySelector(`[${field}]`).parentElement.parentElement
    let $messageNode = $inputParentField.querySelector('.info')

    if ( !$messageNode ){ 
      const info = document.createElement('span')
      info.classList.add('info')
      $inputParentField.append(info) 
    }

    $messageNode = $inputParentField.querySelector('.info')

    if ( isValid) {
      $messageNode.classList.add('success')
      $messageNode.classList.remove('error')
      $form.querySelector(`[${field}]`).value = ""
      setTimeout(() => {
        $messageNode.remove()
      }, "3000");
    } else {
        $messageNode.classList.add('error')
        $messageNode.classList.remove('success')
    }
    
    $messageNode.textContent = message
  }

  const removeInfo = (form, field)=>{
    const $messageNode = form.querySelector(`[${field}]`).parentElement.parentElement.querySelector('.info')
    if ($messageNode) { $messageNode.remove() }
  }

  const ajaxRequest = (data)=>{
    const xhr = new XMLHttpRequest()

    xhr.open('POST', 'send-message', true)
    xhr.setRequestHeader('X-CSRFToken', getToken($contactUsForm))
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    xhr.send(JSON.stringify(data))

    console.log(data)

    xhr.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
          const response = JSON.parse(this.responseText)
          console.log(response)
      }
    }
  }

  const clientValidation = (form, data) => {
    let isAllFilled = true

    const regexValidation = (form, field, value) => {
      const passwordRegex = /^\+?[1-9][0-9]{7,14}$/
      const emailRegex = /^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/

      if ( field === 'data-phone' ) {
        if ( !passwordRegex.test(value) ) {
          showInfo(false, 'The phone number format is invalid.', form, field)
          isAllFilled = false
        }
      }

      if ( field === 'data-email' ) {
        if ( !emailRegex.test(value) ) {
          showInfo(false, 'The e-mail address format is invalid.', form, field)
          isAllFilled = false
        }
      }
    }

    if ( data.url !== '' ) {
      return false
    }
    const newData = { ...data }
    delete newData.url
    

    Object.entries(newData).forEach(([key, value]) => {
      if ( value[0] === '' ) {
        showInfo(false, `Empty ${value[2]} field`, form, value[1])
        isAllFilled = false
      } else {
        removeInfo(form, value[1])
        regexValidation(form, value[1], value[0])
      }
    })

    if ( isAllFilled ) {
      ajaxRequest(data)
    }
  }

  $contactUsForm.addEventListener('submit', e =>{
    e.preventDefault()
    const $fullNameInput = $contactUsForm.querySelector('[data-fullname]')
    const $fullNameLabel = $contactUsForm.querySelector('[data-fullname]').parentElement.parentElement.querySelector('label').textContent
    const $phoneInput = $contactUsForm.querySelector('[data-phone]')
    const $phoneLabel = $contactUsForm.querySelector('[data-phone]').parentElement.parentElement.querySelector('label').textContent
    const $emailInput = $contactUsForm.querySelector('[data-email]')
    const $emailLabel = $contactUsForm.querySelector('[data-email]').parentElement.parentElement.querySelector('label').textContent
    const $contentInput = $contactUsForm.querySelector('[data-content]')
    const $contentLabel = $contactUsForm.querySelector('[data-content]').parentElement.parentElement.querySelector('label').textContent
    const $urlInput = $contactUsForm.querySelector('[name="url"]')

    const data = {
      "fullName": [$fullNameInput.value, 'data-fullname', $fullNameLabel],
      "phone": [$phoneInput.value, 'data-phone', $phoneLabel],
      "email": [$emailInput.value, 'data-email', $emailLabel],
      "content": [$contentInput.value, 'data-content', $contentLabel],
      "url": $urlInput.value,
    }
    
    clientValidation($contactUsForm, data)
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