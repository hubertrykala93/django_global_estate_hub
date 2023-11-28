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
   * Forms reusable functions
    */

const removeInfo = (form, field)=>{
  const $messageNode = form.querySelector(`[${field}]`).parentElement.parentElement.querySelector('.info')
  if ($messageNode) { $messageNode.remove() }
}

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

const clientValidation = (form, data) => {
  let isAllValid = true

  const regexValidation = (form, field, value) => {
    const phoneRegex = /^\+?[1-9][0-9]{7,14}$/
    const emailRegex = /^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/
    const passwordRegex = /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$/

    if ( field === 'data-username' ) {
      if ( value.length < 8 ) {
        showInfo(false, `The ${data.userName[2]} should contain at least 8 characters.`, form, field)
        isAllValid = false
      }
    }

    if ( field === 'data-phone' ) {
      if ( !phoneRegex.test(value) ) {
        showInfo(false, `The ${data.phone[2]} format is invalid.`, form, field)
        isAllValid = false
      }
    }

    if ( field === 'data-email' ) {
      if ( !emailRegex.test(value) ) {
        showInfo(false, `The ${data.email[2]} format is invalid.`, form, field)
        isAllValid = false
      }
    }

    if ( field === 'data-password' ) {
      if ( !passwordRegex.test(value) ) {
        showInfo(false, `The ${data.password[2]} should be at least 8 characters long, including at least one uppercase letter, one lowercase letter, one digit, and one special character.`, form, field)
        isAllValid = false
      }
    }

    if ( field === 'data-password1' ) {
      if ( !passwordRegex.test(value) ) {
        showInfo(false, `The ${data.password1[2]} should be at least 8 characters long, including at least one uppercase letter, one lowercase letter, one digit, and one special character.
        `, form, field)
        isAllValid = false
      }
    }

    if ( field === 'data-password2' ) {
      if ( data.password1[0] != value ) {
        showInfo(false, `The ${data.password2[2]} field does not match the previously entered password.`, form, field)
        isAllValid = false
      }
    }

    if ( field === 'data-checkbox' ) {
      if ( value === false ) {
        showInfo(false, `The ${data.terms[2]} checkbox must be accepted.`, form, field)
        isAllValid = false
      }
    }
  }

  if ( data.url !== '' ) {
    return false
  }
  const newData = { ...data }
  delete newData.url

  Object.entries(newData).forEach(([key, value]) => {
    if ( !Array.isArray(value) ) { return false }
    if ( value[0] === '' ) {
      showInfo(false, `The ${value[2]} field cannot be empty.`, form, value[1])
      isAllValid = false
    } else {
      removeInfo(form, value[1])
      regexValidation(form, value[1], value[0])
    }
  })

  if ( isAllValid ) {
    return true
  }
}

const clearFormValues = (form) => {
  const allInputs = form.querySelectorAll('[data-input]')

  if ( allInputs.length ) {
    allInputs.forEach(input => {
      input.value = ''
    });
  }
}

const successfullySentMessage = (form, message, hide)=>{
  const messageContainer = document.createElement('div')
  messageContainer.classList.add('form__sent-message')
  messageContainer.textContent = message

  form.append(messageContainer)
  if (hide) {
    setTimeout(() => {
      form.querySelector('.form__sent-message').remove()
    }, 2500);
  }
}

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
   * Register form
    */

const $signUpForm = document.querySelector('[data-signup-form]')

if ($signUpForm){

  const serverResponse = (response, data)=> {
    let isSent = true
    if ( response.valid === null ) {
      return false
    } else{
      response.forEach(item => {
        if ( !item.valid ) {
          isSent = false
          showInfo(item.valid, item.message, $signUpForm, item.field)
        } else {
          removeInfo($signUpForm, item.field)
        }
      })
      if (isSent) { 
        clearFormValues($signUpForm)
        successfullySentMessage($signUpForm, `The activation link has been sent to ${data.email[0]}.`, false)
      }
    }
  }

  const ajaxRequest = (data)=>{
    const xhr = new XMLHttpRequest()
    xhr.open('POST', 'create-user', true)
    xhr.setRequestHeader('X-CSRFToken', getToken($signUpForm))
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    xhr.send(JSON.stringify(data))

    xhr.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
          const response = JSON.parse(this.responseText)
          serverResponse(response, data)
      }
    }
  }

  $signUpForm.addEventListener('submit', function (e) {
    e.preventDefault()
    const $userNameInput = this.querySelector('[data-username]')
    const userNameLabel = $userNameInput.parentElement.parentElement.querySelector('label').textContent
    const $emailInput = this.querySelector('[data-email]')
    const emailLabel = $emailInput.parentElement.parentElement.querySelector('label').textContent
    const $password1Input = this.querySelector('[data-password1]')
    const password1Label = $password1Input.parentElement.parentElement.querySelector('label').textContent
    const $password2Input = this.querySelector('[data-password2]')
    const password2Label = $password2Input.parentElement.parentElement.querySelector('label').textContent
    const $termsInput = this.querySelector('[data-checkbox]')
    const $urlInput = this.querySelector('[name="url"]')

    const data = {
      "userName": [$userNameInput.value.trim(), "data-username", userNameLabel],
      "email": [$emailInput.value.trim(), "data-email", emailLabel],
      "password1": [$password1Input.value.trim(), "data-password1", password1Label],
      "password2": [$password2Input.value.trim(), "data-password2", password2Label],
      "terms": [$termsInput.checked, "data-checkbox", 'terms'],
      "url": $urlInput.value,
    }
    
    if ( clientValidation($signUpForm, data) ) {
      ajaxRequest(data)
    }
  })
}


/**
   * Login form
    */

const $loginForm = document.querySelector('[data-login-form]')

if ($loginForm){

  const serverResponse = (response)=> {
    let isSent = true
    if ( response.valid === null ) {
      return false
    } else{
      response.forEach(item => {
        if ( !item.valid ) {
          isSent = false
          showInfo(item.valid, item.message, $loginForm, item.field)
        } else {
          removeInfo($loginForm, item.field)
        }
      })
      if (isSent) { 
        location.href = '/'
      }
    }
  }

  const ajaxRequest = (data)=>{
    const xhr = new XMLHttpRequest()
    xhr.open('POST', 'authorization', true)
    xhr.setRequestHeader('X-CSRFToken', getToken($loginForm))
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

  $loginForm.addEventListener('submit', function (e) {
    e.preventDefault()
    const $emailInput = this.querySelector('[data-email]')
    const emailLabel = $emailInput.parentElement.parentElement.querySelector('label').textContent
    const $passwordInput = this.querySelector('[data-password]')
    const passwordLabel = $passwordInput.parentElement.parentElement.querySelector('label').textContent
    const $urlInput = this.querySelector('[name="url"]')

    const data = {
      "email": [$emailInput.value.trim(), "data-email", emailLabel],
      "password": [$passwordInput.value.trim(), "data-password", passwordLabel],
      "url": $urlInput.value
    }

    if ( clientValidation($loginForm, data) ) {
      ajaxRequest(data)
    }

  })
}


/**
   * Forgot password
    */

const $forgotPasswordWrapper = document.querySelector('[data-forgot-password-wrapper]')

if ($forgotPasswordWrapper){

  let currentStep = 1
  const $allSteps = $forgotPasswordWrapper.querySelectorAll('[data-step-slide]')
  const allStepsLenght = $allSteps.length

  const goToNextStep = (nextStepCallback) => {
      const $currentStep = $allSteps[currentStep - 1]
      const $nextStep = $allSteps[currentStep]
      $nextStep.style.zIndex = 2
      $nextStep.style.transform = "translateX(0)"
      setTimeout(() => {
        $currentStep.style.position = "absolute"
        $nextStep.style.position = "relative"
      }, 400);
      currentStep++
      nextStepCallback()
  }

  const firstStepServerResponse = (response, form) => {
    if ( response.valid === false ) {
      showInfo(response.valid, response.message, form, 'data-email')
    } else{
      sessionStorage.setItem('verifyingEmail', response.email)
      goToNextStep(secondStep)
    }
  }

  const firstStepAjaxRequest = (data, form) =>{
    const xhr = new XMLHttpRequest()
    xhr.open('POST', 'send-password', true)
    xhr.setRequestHeader('X-CSRFToken', getToken(form))
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    xhr.send(JSON.stringify(data))

    xhr.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
          const response = JSON.parse(this.responseText)
          firstStepServerResponse(response, form)
      }
    }
  }

  const secondStepServerResponse = (response, form) => {
    if ( response.valid === false ) {
      showInfo(response.valid, response.message, form, 'data-code')
    } else{
      sessionStorage.setItem('verifyingEmail', response.email)
      goToNextStep(thirdStep)
    }
  }

  const secondStepAjaxRequest = (data, form) =>{
    const xhr = new XMLHttpRequest()
    xhr.open('POST', 'validate-password', true)
    xhr.setRequestHeader('X-CSRFToken', getToken(form))
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    xhr.send(JSON.stringify(data))

    xhr.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
          const response = JSON.parse(this.responseText)
          secondStepServerResponse(response, form)
      }
    }
  }

  const thirdStepServerResponse = (response, form)=> {
    let isSent = true
    if ( response.valid === null ) {
      return false
    } else{
      response.forEach(item => {
        if ( !item.valid ) {
          isSent = false
          showInfo(item.valid, item.message, form, item.field)
        } else {
          removeInfo(form, item.field)
        }
      })
      if (isSent) { 
        
      }
    }
  }
  
  const thirdStepAjaxRequest = (data, form) =>{
    const xhr = new XMLHttpRequest()
    xhr.open('PATCH', 'set-password', true)
    xhr.setRequestHeader('X-CSRFToken', getToken(form))
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    xhr.send(JSON.stringify(data))

    xhr.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
          const response = JSON.parse(this.responseText)
          console.log('odebrane dane', response)
          // thirdStepServerResponse(response, form)
      }
    }
  }






  //3rd step
  // const thirdStep = ()=> {
  //   const $newPasswordForm = $forgotPasswordWrapper.querySelector('[data-new-password-form]')



  //   const thirdStepValidation = ($form, response) => {
  //     const fieldsNumber = response.length
  //     let validFields = 0
    
  //     response.forEach(field => {
  //       const $currentformField = $form.querySelector(`[${field.field}]`).closest('.form__field')
  //       const $message = $currentformField.querySelector('.info')
  //       if (field.valid == false) {
  //         const $message = $currentformField.querySelector('.info')
  //         validFields = 0
    
  //         if($message){ 
  //           $message.textContent = field.message 
  //         }else {
  //           const info = document.createElement('span')
  //           info.classList.add('info')
  //           info.classList.add('error')
  //           info.textContent = field.message
  //           $currentformField.append(info)
  //         }
  //       } else{
  //         validFields++
  //         if($message){ 
  //           $message.remove()
  //         }
  //       }
  //       if ( validFields === fieldsNumber ) {
  //         goToStepFour()
  //       }
  //     });
  //   }

  //   $newPasswordForm.addEventListener('submit', function (e) {
  //     e.preventDefault()
  //     let csrftoken = this.querySelector('[name="csrftoken"]').value
  //     const $password1Input = $newPasswordForm.querySelector('[data-password1]')
  //     const $password2Input = $newPasswordForm.querySelector('[data-password2]')
  //     const data = {
  //       "password1": [$password1Input.value, "data-password1"],
  //       "password2": [$password2Input.value, "data-password2"],
  //       "email": sessionStorage.getItem('verifyingEmail')
  //     }
        
  //     const xhr = new XMLHttpRequest()
  //     xhr.open('PATCH', 'set-password', true)
  //     xhr.setRequestHeader('X-CSRFToken', csrftoken)
  //     xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
  //     xhr.send(JSON.stringify(data))
  
  //     xhr.onreadystatechange = function () {
  //       if (this.readyState == 4 && this.status == 200) {
  //           const response = JSON.parse(this.responseText)
  //           thirdStepValidation($newPasswordForm, response)
  //       }
  //     }
  //   })
  // }


  //2nd step
  // const secondSteps = ()=> {
  //   // const $verificationForm = $forgotPasswordWrapper.querySelector('[data-verification-password-form]')
  //   // const $veryfyingEmail = $forgotPasswordWrapper.querySelector('[data-verification-email]')
  //   // const $verificationFormInputs = $verificationForm.querySelectorAll('[data-code]')

  //   // $veryfyingEmail.textContent = sessionStorage.getItem('verifyingEmail')

  //   // $verificationFormInputs.forEach((input, index) => {
  //   //   input.addEventListener('input', ()=>{
  //   //     if ( !input.value.match(/^[0-9]+$/) ) {
  //   //       input.value = ''
  //   //       input.classList.remove('highlighted')
  //   //     } else {
  //   //       input.classList.add('highlighted')
  //   //       const inputToFocus = index + 1 < $verificationFormInputs.length ? index + 1 : false
  //   //       if (inputToFocus) { $verificationFormInputs[inputToFocus].focus() }
  //   //     }
  //   //   })
  //   // })

  //   $verificationForm.addEventListener('submit', function (e) {
  //     e.preventDefault()
  //     const $codeInputs = this.querySelectorAll('[data-code]')
  //     let filledInputs = 0
  //     let typedCode = ""
  //     $codeInputs.forEach(input=> {
  //       if (input.value !== ''){
  //         filledInputs++
  //         typedCode += input.value
  //       }
  //     })

  //     if ( filledInputs !== $codeInputs.length ) {
  //       secondStepValidation($verificationForm, "Fill all inputs.")
  //     } else {
  //       const data = {
  //         "code": typedCode,
  //         "email": sessionStorage.getItem('verifyingEmail')
  //       }
        
  //       const xhr = new XMLHttpRequest()
  //       xhr.open('POST', 'validate-password', true)
  //       xhr.setRequestHeader('X-CSRFToken', csrftoken)
  //       xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
  //       xhr.send(JSON.stringify(data))
    
  //       xhr.onreadystatechange = function () {
  //         if (this.readyState == 4 && this.status == 200) {
  //             const response = JSON.parse(this.responseText)
    
  //             if( response.valid == true ) {
  //               sessionStorage.setItem('verifyingEmail', response.email)
  //               goToStepThree()
  //             } else{
  //               secondStepValidation($verificationForm, response.message)
  //             }
  //         }
  //       }
  //     }
  //   })
  // }




  //1st step
  const $forgotPasswordForm = $forgotPasswordWrapper.querySelector('[data-forgot-password-form]')

  $forgotPasswordForm.addEventListener('submit', function (e) {
    e.preventDefault()
    const $emailInput = this.querySelector('[data-email]')
    const emailLabel = $emailInput.parentElement.parentElement.querySelector('label').textContent
    const $urlInput = this.querySelector('[name="url"]')

    const data = {
      "email": [$emailInput.value.trim(), 'data-email', emailLabel],
      "url": $urlInput.value
    }
    
    if ( clientValidation($forgotPasswordForm, data) ) {
      firstStepAjaxRequest(data, $forgotPasswordForm)
    }
  })

  //2nd step
  function secondStep (){
    const $verificationForm = $forgotPasswordWrapper.querySelector('[data-verification-password-form]')
    const $veryfyingEmail = $forgotPasswordWrapper.querySelector('[data-verification-email]')
    const $verificationFormInputs = $verificationForm.querySelectorAll('[data-code]')

    $veryfyingEmail.textContent = sessionStorage.getItem('verifyingEmail')

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
        showInfo(false, 'Fill all inputs.', $verificationForm, 'data-code')
      } else {
        const $urlInput = this.querySelector('[name="url"]')

        const data = {
          "code": typedCode,
          "email": sessionStorage.getItem('verifyingEmail'),
          "url": $urlInput.value
        }

        if ( data.url === '' ) { secondStepAjaxRequest(data, $verificationForm) }
      }
    })
  }

  //3rd step
  function thirdStep (){
    const $newPasswordForm = $forgotPasswordWrapper.querySelector('[data-new-password-form]')

    $newPasswordForm.addEventListener('submit', function (e) {
      e.preventDefault()
      const $password1Input = this.querySelector('[data-password1]')
      const password1Label = $password1Input.parentElement.parentElement.querySelector('label').textContent
      const $password2Input = this.querySelector('[data-password2]')
      const password2Label = $password2Input.parentElement.parentElement.querySelector('label').textContent
      const $urlInput = this.querySelector('[name="url"]')

      const data = {
        "password1": [$password1Input.value, "data-password1", password1Label],
        "password2": [$password2Input.value, "data-password2", password2Label],
        "email": sessionStorage.getItem('verifyingEmail'),
        "url": $urlInput.value
      }

      if ( clientValidation($newPasswordForm, data) ) {
        console.log('wysłane dane', data)
        thirdStepAjaxRequest(data, $newPasswordForm)
      }
        
    })
  }
}


/**
  * Contact us form
   */

const $contactUsForm = document.querySelector('[data-contact-form]')

if ($contactUsForm) {

  const ajaxRequest = (data)=>{
    const xhr = new XMLHttpRequest()

    xhr.open('POST', 'send-message', true)
    xhr.setRequestHeader('X-CSRFToken', getToken($contactUsForm))
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

  const serverResponse = (response)=> {
    let isSent = true
    if ( response.valid === null ) {
      return false
    } else{
      response.forEach(item => {
        if ( !item.valid ) {
          isSent = false
          showInfo(item.valid, item.message, $contactUsForm, item.field)
        } else {
          removeInfo($contactUsForm, item.field)
        }
      })
      if (isSent) { 
        clearFormValues($contactUsForm)
        successfullySentMessage($contactUsForm, 'The message has been sent successfully, we will respond shortly.', true)
      }
    }
  }

  $contactUsForm.addEventListener('submit', function(e) {
    e.preventDefault()
    const $fullNameInput = this.querySelector('[data-fullname]')
    const $fullNameLabel = $fullNameInput.parentElement.parentElement.querySelector('label').textContent
    const $phoneInput = this.querySelector('[data-phone]')
    const $phoneLabel = $phoneInput.parentElement.parentElement.querySelector('label').textContent
    const $emailInput = this.querySelector('[data-email]')
    const $emailLabel = $emailInput.parentElement.parentElement.querySelector('label').textContent
    const $contentInput = this.querySelector('[data-content]')
    const $contentLabel = $contentInput.parentElement.parentElement.querySelector('label').textContent
    const $urlInput = $contactUsForm.querySelector('[name="url"]')

    const data = {
      "fullName": [$fullNameInput.value.trim(), 'data-fullname', $fullNameLabel],
      "phone": [$phoneInput.value.trim(), 'data-phone', $phoneLabel],
      "email": [$emailInput.value.trim(), 'data-email', $emailLabel],
      "content": [$contentInput.value.trim(), 'data-content', $contentLabel],
      "url": $urlInput.value,
    }
    
    if( clientValidation($contactUsForm, data) ) {
      ajaxRequest(data)
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

/**
   * Contact map
    */

const $contactMap = document.querySelector('[data-contact-map]')

if ($contactMap) {
  const map = L.map('map').setView([-37.79347799465808, 144.97906345418576], 13)
  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  }).addTo(map)
  const mapMArker = L.icon({
    iconUrl: '/media/icons/map-marker.svg',

    iconSize:     [41, 59],
    iconAnchor:   [41, 59],
  });
  const marker = L.marker([-37.79347799465808, 144.97906345418576], {icon: mapMArker}).addTo(map);
}