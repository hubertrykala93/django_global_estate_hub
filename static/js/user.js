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
    xhr.setRequestHeader('X-CSRFToken', csrfToken)
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
    const urlValue = this.querySelector('[name="url"]').value
    if ( !urlValue == '' ) { return false }

    const $userNameInput = this.querySelector('[data-username]')
    const userNameLabel = $userNameInput.parentElement.parentElement.querySelector('label').textContent
    const $emailInput = this.querySelector('[data-email]')
    const emailLabel = $emailInput.parentElement.parentElement.querySelector('label').textContent
    const $password1Input = this.querySelector('[data-password1]')
    const password1Label = $password1Input.parentElement.parentElement.querySelector('label').textContent
    const $password2Input = this.querySelector('[data-password2]')
    const password2Label = $password2Input.parentElement.parentElement.querySelector('label').textContent
    const $termsInput = this.querySelector('[data-checkbox]')

    const data = {
      "userName": [$userNameInput.value.trim(), "data-username", userNameLabel],
      "email": [$emailInput.value.trim(), "data-email", emailLabel],
      "password1": [$password1Input.value.trim(), "data-password1", password1Label],
      "password2": [$password2Input.value.trim(), "data-password2", password2Label],
      "terms": [$termsInput.checked, "data-checkbox", 'terms'],
      "accountType": [getRadioValue($signUpForm, 'data-account-type'), "data-account-type", 'account type'],
      "url": urlValue,
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
    xhr.setRequestHeader('X-CSRFToken', csrfToken)
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
    const urlValue = this.querySelector('[name="url"]').value
    if ( !urlValue == '' ) { return false }

    const $emailInput = this.querySelector('[data-email]')
    const emailLabel = $emailInput.parentElement.parentElement.querySelector('label').textContent
    const $passwordInput = this.querySelector('[data-password]')
    const passwordLabel = $passwordInput.parentElement.parentElement.querySelector('label').textContent

    const data = {
      "email": [$emailInput.value.trim(), "data-email", emailLabel],
      "password": [$passwordInput.value.trim(), "data-password", passwordLabel],
      "url": urlValue
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
      if (nextStepCallback) {nextStepCallback()}
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
    xhr.setRequestHeader('X-CSRFToken', csrfToken)
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
    xhr.setRequestHeader('X-CSRFToken', csrfToken)
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
        goToNextStep()
      }
    }
  }
  
  const thirdStepAjaxRequest = (data, form) =>{
    const xhr = new XMLHttpRequest()
    xhr.open('PATCH', 'set-password', true)
    xhr.setRequestHeader('X-CSRFToken', csrfToken)
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    xhr.send(JSON.stringify(data))

    xhr.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
          const response = JSON.parse(this.responseText)
          thirdStepServerResponse(response, form)
      }
    }
  }


  //1st step
  const $forgotPasswordForm = $forgotPasswordWrapper.querySelector('[data-forgot-password-form]')

  $forgotPasswordForm.addEventListener('submit', function (e) {
    e.preventDefault()
    const urlValue = this.querySelector('[name="url"]').value
    if ( !urlValue == '' ) { return false }

    const $emailInput = this.querySelector('[data-email]')
    const emailLabel = $emailInput.parentElement.parentElement.querySelector('label').textContent

    const data = {
      "email": [$emailInput.value.trim(), 'data-email', emailLabel],
      "url": urlValue
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
      const urlValue = this.querySelector('[name="url"]').value
      if ( !urlValue == '' ) { return false }

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

        const data = {
          "code": typedCode,
          "email": sessionStorage.getItem('verifyingEmail'),
          "url": urlValue
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
      const urlValue = this.querySelector('[name="url"]').value
      if ( !urlValue == '' ) { return false }

      const $password1Input = this.querySelector('[data-password1]')
      const password1Label = $password1Input.parentElement.parentElement.querySelector('label').textContent
      const $password2Input = this.querySelector('[data-password2]')
      const password2Label = $password2Input.parentElement.parentElement.querySelector('label').textContent

      const data = {
        "password1": [$password1Input.value, "data-password1", password1Label],
        "password2": [$password2Input.value, "data-password2", password2Label],
        "email": sessionStorage.getItem('verifyingEmail'),
        "url": urlValue
      }

      if ( clientValidation($newPasswordForm, data) ) {
        thirdStepAjaxRequest(data, $newPasswordForm)
      }
        
    })
  }
}

/*----------------------------------*\
  #ACCOUNT SETTINGS
\*----------------------------------*/

const $accountSettings = document.querySelector('[data-account-settings]')

if ($accountSettings){

  /**
   * Tabs
    */

  const tabContents = $accountSettings.querySelectorAll('[data-tab-content]')
  const nav = $accountSettings.querySelector('[data-account-tabs]')
  const contentTitleAnimation = {
    delay: 100,
    distance: '30px',
    duration: 400,
    opacity: .01,
    origin: 'bottom',
    easing: 'linear'
  }

  nav.addEventListener('click', e => {
    if ( e.target.dataset.hasOwnProperty('accountTab') ) {
      const tabId = e.target.dataset.accountTab
      nav.querySelectorAll('[data-account-tab]').forEach(btn => {
        btn.classList.remove('active')
      })
      e.target.classList.add('active')

      tabContents.forEach(content => {
        if ( content.dataset.tabContent === tabId ) {
          content.classList.add('active')
          const contentTitle = content.querySelector('[data-title]')
          
          ScrollReveal().reveal(contentTitle, contentTitleAnimation)
          ScrollReveal().reveal(contentTitle, { afterReveal: function (el) {
            ScrollReveal().clean(el)
            el.removeAttribute('style')
          } })
        } else {
          content.classList.remove('active')
        }
      })
    }
  })

  /**
   * Account settings forms
    */

  //User settings - avatar
  const $avatarForm = $accountSettings.querySelector('[data-upload-avatar-form]')
  const $fileInput = $avatarForm.querySelector('[data-avatar]')
  const $uploadButton = $avatarForm.querySelector('[data-upload-avatar]')
  const avatarformats = ['jpg', 'jpeg', 'webp', 'png', 'svg']

  const showAvatarMessage = (isValid, message) => {
    let $messageNode = $avatarForm.querySelector('.info')

    if ( !$messageNode ){ 
      const info = document.createElement('span')
      info.classList.add('info')
      $avatarForm.append(info) 
      $messageNode = $avatarForm.querySelector('.info')
    }

    if ( isValid) {
      $messageNode.classList.add('success')
      $messageNode.classList.remove('error')
      setTimeout(() => {
        $messageNode.remove()
      }, "3000");
    } else {
        $messageNode.classList.add('error')
        $messageNode.classList.remove('success')
    }

    $messageNode.textContent = message
  }

  const uploadAvatarServerResponse = (response) =>{
    if ( !response.valid ) {
      showAvatarMessage(response.valid, response.message)
      return false
    }

    const $avatarLoader = $avatarForm.querySelector('[data-avatar-loader]')
    const $avatarImage = $avatarForm.querySelector('[data-avatar-image]')
    $avatarLoader.classList.add('active')
    $avatarImage.src = response.path
    setTimeout(() => {
      $avatarLoader.classList.remove('active')
    }, "3000");
    showAvatarMessage(response.valid, response.message)
  }

  const uploadAvatarAjaxRequest = (data) => {
    const xhr = new XMLHttpRequest()
  
    xhr.open('POST', 'upload-avatar', true)
    xhr.setRequestHeader('X-CSRFToken', csrfToken)
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    xhr.send(data)

    xhr.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
          const response = JSON.parse(this.responseText)
          uploadAvatarServerResponse(response)
      }
    }
  }
  
  $uploadButton.addEventListener('click', () => {
    $fileInput.click()
  })
  
  $avatarForm.addEventListener('change', () =>{
    const file = $fileInput.files[0]

    if (file) {
      const fileFormat = file.name.slice(file.name.lastIndexOf('.') + 1)
      
      if ( !avatarformats.includes(fileFormat) ) {
        showAvatarMessage(false, 'Invalid file format. The file format should be jpg, jpeg, webp, png, svg.')
        return false
      }
      
      if ( (file.size / 1024 / 1024) > 1 ) {
        showAvatarMessage(false, 'The file size should not exceed 1 MB.')
        return false
      }
      
      let $messageNode = $avatarForm.querySelector('.info')
      if( $messageNode ) { $messageNode.remove() }

      const data = new FormData()
      data.append('file', file)
      uploadAvatarAjaxRequest(data)
    }
  })

  //User settings - form
  const $userSettingsForm = $accountSettings.querySelector('[data-user-settings-form]')
  let currentUsername = $userSettingsForm.querySelector('[data-username]').value
  let currentEmail = $userSettingsForm.querySelector('[data-email]').value

  const userSettingsServerResponse = (response)=> {
    response.forEach(field => {
      if ( field.message === '' ) { 
        removeInfo($userSettingsForm, field.field) 
      }else {
        showInfo(field.valid, field.message, $userSettingsForm, field.field)
        
        if ( field.valid ) {
          if ( field.field === 'data-username') {
            $userSettingsForm.querySelector(`[${field.field}]`).value = field.value
            currentUsername = field.value
          }
          if ( field.field === 'data-email') {
            $userSettingsForm.querySelector(`[${field.field}]`).value = field.value
            currentEmail = field.value
          }
        }
      }
    })
  }

  const userSettingsAjaxRequest = (data) =>{
    const xhr = new XMLHttpRequest()

    xhr.open('PATCH', 'user-settings', true)
    xhr.setRequestHeader('X-CSRFToken', csrfToken)
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    xhr.send(JSON.stringify(data))

    xhr.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
          const response = JSON.parse(this.responseText)
          userSettingsServerResponse(response)
      }
    }
  }

  const userSettingsClientValidation = (data)=>{
    let isAllValid = true
    let isAllEmpty = true

    const regexValidation = (form, field, value) => {
      const emailRegex = /^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/
      const passwordRegex = /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$/

      if ( field === 'data-username' ) {
        if ( value.length < 8 ) {
          showInfo(false, `The ${data.username[2]} should contain at least 8 characters.`, form, field)
          isAllValid = false
        } else {
          removeInfo(form, field)
        }
      }


      if ( field === 'data-email' ) {
        if ( !emailRegex.test(value) ) {
          showInfo(false, `The ${data.email[2]} format is invalid.`, form, field)
          isAllValid = false
        } else {
          removeInfo(form, field)
        }
      }

      if ( field === 'data-password1' ) {
        if ( !passwordRegex.test(value) ) {
          showInfo(false, `The ${data.password1[2]} should be at least 8 characters long, including at least one uppercase letter, one lowercase letter, one digit, and one special character.
          `, form, field)
          isAllValid = false
        } else {
          removeInfo(form, field)
        }
      }

      if ( field === 'data-password2' ) {
        if ( data.password1[0] != value ) {
          showInfo(false, `The ${data.password2[2]} field does not match the previously entered password.`, form, field)
          isAllValid = false
        } else {
          removeInfo(form, field)
        }
      }
    }

    Object.entries(data).forEach(([key, value]) => {
      if( value[0] !== '' ) {
        regexValidation($userSettingsForm, value[1], value[0])
        isAllEmpty = false
      }
    })

    if ( isAllValid && !isAllEmpty) {
      return true
    }
  }

  $userSettingsForm.addEventListener('submit', function (e) {
    e.preventDefault()
    const $usernameInput = this.querySelector('[data-username]')
    const usernameLabel = $usernameInput.parentElement.parentElement.querySelector('.form__label').textContent
    const usernameValue = $usernameInput.value.trim() !== currentUsername ? $usernameInput.value.trim() : ''

    const $emailInput = this.querySelector('[data-email]')
    const emailLabel = $emailInput.parentElement.parentElement.querySelector('.form__label').textContent
    const emailValue = $emailInput.value.trim() !== currentEmail ? $emailInput.value.trim() : ''

    const $password1Input = this.querySelector('[data-password1]')
    const password1Label = $password1Input.parentElement.parentElement.querySelector('.form__label').textContent
    const password1Value = $password1Input.value.trim()

    const $password2Input = this.querySelector('[data-password2]')
    const password2Label = $password2Input.parentElement.parentElement.querySelector('.form__label').textContent
    const password2Value = $password2Input.value.trim()

    const data = {
      "username": [usernameValue, "data-username", usernameLabel],
      "email": [emailValue, "data-email", emailLabel],
      "password1": [password1Value, "data-password1", password1Label],
      "password2": [password2Value, "data-password2", password2Label],
    }

    if ( userSettingsClientValidation(data) ) {
      userSettingsAjaxRequest(data)
    }
    
  })

  //Profile settings - form
  const $profileSettingsForm = $accountSettings.querySelector('[data-profile-settings-form]')
  let currentFirstName = ''
  let currentLastName = ''
  let currentGender = ''
  let currentCompanyName = ''
  let currentCompanyId = ''
  let currentPhone = $profileSettingsForm.querySelector('[data-phone]').value
  
  if ($profileSettingsForm.querySelector('[data-firstname]')) {
    currentFirstName = $profileSettingsForm.querySelector('[data-firstname]').value
  }
  if ($profileSettingsForm.querySelector('[data-lastname]')) {
    currentLastName = $profileSettingsForm.querySelector('[data-lastname]').value
  }
  if ($profileSettingsForm.querySelector('[data-gender]')) {
    currentGender = getRadioValue($profileSettingsForm, 'data-gender')
  }
  if ($profileSettingsForm.querySelector('[data-company-name]')) {
    currentCompanyName = $profileSettingsForm.querySelector('[data-company-name]').value
  }
  if ($profileSettingsForm.querySelector('[data-company-id]')) {
    currentCompanyId = $profileSettingsForm.querySelector('[data-company-id]').value
  }

  const profileSettingsServerResponse = (response)=> {
    response.forEach(field => {
      if ( field.message === '' ) { 
        removeInfo($profileSettingsForm, field.field) 
      }else {
        showInfo(field.valid, field.message, $profileSettingsForm, field.field)
        
        if ( field.valid ) {
          if ( field.field === 'data-firstname') {
            $profileSettingsForm.querySelector(`[${field.field}]`).value = field.value
            currentFirstName = field.value
          }
          if ( field.field === 'data-lastname') {
            $profileSettingsForm.querySelector(`[${field.field}]`).value = field.value
            currentLastName = field.value
          }
          if ( field.field === 'data-gender') {
            $profileSettingsForm.querySelectorAll(`[${field.field}]`).forEach(input => { 
              if ( input.value === field.value) { input.checked = true }
             })
            currentGender = field.value
          }
          if ( field.field === 'data-company-name') {
            $profileSettingsForm.querySelector(`[${field.field}]`).value = field.value
            currentCompanyName = field.value
          }
          if ( field.field === 'data-company-id') {
            $profileSettingsForm.querySelector(`[${field.field}]`).value = field.value
            currentCompanyId = field.value
          }
          if ( field.field === 'data-phone') {
            $profileSettingsForm.querySelector(`[${field.field}]`).value = field.value
            currentPhone = field.value
          }
        }
      }
    })
  }

  const profileSettingsAjaxRequest = (data) =>{
    const xhr = new XMLHttpRequest()

    xhr.open('PATCH', 'profile-settings', true)
    xhr.setRequestHeader('X-CSRFToken', csrfToken)
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    xhr.send(JSON.stringify(data))

    xhr.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
          const response = JSON.parse(this.responseText)
          profileSettingsServerResponse(response)
      }
    }
  }

  const profileSettingsClientValidation = (data)=>{
    let isAllValid = true
    let isAllEmpty = true

    const regexValidation = (form, field, value) => {
      const phoneRegex = /^\+?[1-9][0-9]{7,14}$/

      if ( field === 'data-phone' ) {
        if ( !phoneRegex.test(value) ) {
          showInfo(false, `The ${data.phone_number[2]} format is invalid.`, form, field)
          isAllValid = false
        } else {
          removeInfo(form, field)
        }
      }
    }

    Object.entries(data).forEach(([key, value]) => {
      if( value[0] !== '' ) {
        regexValidation($profileSettingsForm, value[1], value[0])
        isAllEmpty = false
      } else {
        removeInfo($profileSettingsForm, value[1])
      }
    })

    if ( isAllValid && !isAllEmpty) {
      return true
    }
  }

  $profileSettingsForm.addEventListener('submit', function (e) {
    e.preventDefault()

    const data = {}
    
    const $firstNameInput = this.querySelector('[data-firstname]')
    if ( $firstNameInput ) {
      const label = $firstNameInput.parentElement.parentElement.querySelector('.form__label').textContent
      const value = $firstNameInput.value.trim() !== currentFirstName ? $firstNameInput.value.trim() : ''
      data.first_name = [value, "data-firstname", label]
    }

    const $lastNameInput = this.querySelector('[data-lastname]')
    if ( $lastNameInput ) {
      const label = $lastNameInput.parentElement.parentElement.querySelector('.form__label').textContent
      const value = $lastNameInput.value.trim() !== currentLastName ? $lastNameInput.value.trim() : ''
      data.last_name = [value, "data-lastname", label]
    }

    const $genderInput = this.querySelector('[data-gender]')
    if ( $genderInput ) {
      const label = $genderInput.closest('.form__field').querySelector('.form__label').textContent
      const value = getRadioValue($profileSettingsForm, 'data-gender') !== currentGender ? getRadioValue($profileSettingsForm, 'data-gender') : ''
      data.gender = [value, "data-gender", label]
    }

    const $companyNameInput = this.querySelector('[data-company-name]')
    if ( $companyNameInput ) {
      const label = $companyNameInput.closest('.form__field').querySelector('.form__label').textContent
      const value = $companyNameInput.value.trim() !== currentCompanyName ? $companyNameInput.value.trim() : ''
      data.company_name = [value, "data-company-name", label]
    }

    const $companyIdInput = this.querySelector('[data-company-id]')
    if ( $companyIdInput ) {
      const label = $companyIdInput.closest('.form__field').querySelector('.form__label').textContent
      const value = $companyIdInput.value.trim() !== currentCompanyId ? $companyIdInput.value.trim() : ''
      data.company_id = [value, "data-company-id", label]
    }
    
    const $phoneInput = this.querySelector('[data-phone]')
    const phoneLabel = $phoneInput.parentElement.parentElement.querySelector('.form__label').textContent
    const phoneValue = $phoneInput.value.trim() !== currentPhone ? $phoneInput.value.trim() : ''
    data.phone_number = [phoneValue, "data-phone", phoneLabel]

    if ( profileSettingsClientValidation(data) ) {
      profileSettingsAjaxRequest(data)
    }
  })

  //Localizations settings / social media - forms
  const $localizationSettingsForm = $accountSettings.querySelector('[data-localization-settings-form]')
  let currentCountry = $localizationSettingsForm.querySelector('[data-country]').value
  let currentProvince = $localizationSettingsForm.querySelector('[data-province]').value
  let currentCity = $localizationSettingsForm.querySelector('[data-city]').value
  let currentStreet = $localizationSettingsForm.querySelector('[data-street]').value
  let currentPostalCode = $localizationSettingsForm.querySelector('[data-postal-code]').value

  const $socialMediaForm = $accountSettings.querySelector('[data-social-media-settings-form]')
  let currentWebsiteUrl = $socialMediaForm.querySelector('[data-website-url]').value
  let currentFacebookUrl = $socialMediaForm.querySelector('[data-facebook-url]').value
  let currentInstagramUrl = $socialMediaForm.querySelector('[data-instagram-url]').value
  let currentLinkedinUrl = $socialMediaForm.querySelector('[data-linkedin-url]').value

  const localizationSocialMediaSettingsServerResponse = (response, form)=> {
    response.forEach(field => {
      if ( field.message === '' ) { 
        removeInfo(form, field.field) 
      }else {
        showInfo(field.valid, field.message, form, field.field)
        
        if ( field.valid ) {
          if ( field.field === 'data-country') {
            form.querySelector(`[${field.field}]`).value = field.value
            currentCountry = field.value
          }
          if ( field.field === 'data-province') {
            form.querySelector(`[${field.field}]`).value = field.value
            currentProvince = field.value
          }
          if ( field.field === 'data-city') {
            form.querySelector(`[${field.field}]`).value = field.value
            currentCity = field.value
          }
          if ( field.field === 'data-street') {
            form.querySelector(`[${field.field}]`).value = field.value
            currentStreet = field.value
          }
          if ( field.field === 'data-postal-code') {
            form.querySelector(`[${field.field}]`).value = field.value
            currentPostalCode = field.value
          }


          if ( field.field === 'data-website-url') {
            form.querySelector(`[${field.field}]`).value = field.value
            currentWebsiteUrl = field.value
          }
          if ( field.field === 'data-facebook-url') {
            form.querySelector(`[${field.field}]`).value = field.value
            currentFacebookUrl = field.value
          }
          if ( field.field === 'data-instagram-url') {
            form.querySelector(`[${field.field}]`).value = field.value
            currentInstagramUrl = field.value
          }
          if ( field.field === 'data-linkedin-url') {
            form.querySelector(`[${field.field}]`).value = field.value
            currentLinkedinUrl = field.value
          }
        }
      }
    })
  }

  const localizationSocialMediaSettingsClientValidation = (data, form)=>{
    let isAllValid = true
    let isAllEmpty = true

    Object.entries(data).forEach(([key, value]) => {
      if( value[0] !== '' ) {
        isAllEmpty = false
      } else {
        removeInfo(form, value[1])
      }
    })

    if ( isAllValid && !isAllEmpty) {
      return true
    }
  }

  const localizationSettingsAjaxRequest = (data) =>{
    const xhr = new XMLHttpRequest()

    xhr.open('PATCH', 'localization-settings', true)
    xhr.setRequestHeader('X-CSRFToken', csrfToken)
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    xhr.send(JSON.stringify(data))

    xhr.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
          const response = JSON.parse(this.responseText)
          localizationSocialMediaSettingsServerResponse(response, $localizationSettingsForm)
      }
    }
  }

  const socialMediaSettingsAjaxRequest = (data) =>{
    const xhr = new XMLHttpRequest()

    xhr.open('PATCH', 'social-media-settings', true)
    xhr.setRequestHeader('X-CSRFToken', csrfToken)
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    xhr.send(JSON.stringify(data))

    xhr.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
          const response = JSON.parse(this.responseText)
          localizationSocialMediaSettingsServerResponse(response, $socialMediaForm)
      }
    }
  }

  $localizationSettingsForm.addEventListener('submit', function (e) {
    e.preventDefault()
    const $countryInput = this.querySelector('[data-country]')
    const countryLabel = $countryInput.parentElement.parentElement.querySelector('.form__label').textContent
    const countryValue = $countryInput.value.trim() !== currentCountry ? $countryInput.value.trim() : ''
    
    const $provinceInput = this.querySelector('[data-province]')
    const provinceLabel = $provinceInput.parentElement.parentElement.querySelector('.form__label').textContent
    const provinceValue = $provinceInput.value.trim() !== currentProvince ? $provinceInput.value.trim() : ''
    
    const $cityInput = this.querySelector('[data-city]')
    const cityLabel = $cityInput.parentElement.parentElement.querySelector('.form__label').textContent
    const cityValue = $cityInput.value.trim() !== currentCity ? $cityInput.value.trim() : ''
    
    const $streetInput = this.querySelector('[data-street]')
    const streetLabel = $streetInput.parentElement.parentElement.querySelector('.form__label').textContent
    const streetValue = $streetInput.value.trim() !== currentStreet ? $streetInput.value.trim() : ''
    
    const $postalCodeInput = this.querySelector('[data-postal-code]')
    const postalCodeLabel = $postalCodeInput.parentElement.parentElement.querySelector('.form__label').textContent
    const postalCodeValue = $postalCodeInput.value.trim() !== currentPostalCode ? $postalCodeInput.value.trim() : ''

    const data = {
      "country": [countryValue, "data-country", countryLabel],
      "province": [provinceValue, "data-province", provinceLabel],
      "city": [cityValue, "data-city", cityLabel],
      "street": [streetValue, "data-street", streetLabel],
      "postal_code": [postalCodeValue, "data-postal-code", postalCodeLabel],
    }

    if ( localizationSocialMediaSettingsClientValidation(data, $localizationSettingsForm) ) {
      localizationSettingsAjaxRequest(data)
    }
    
  })

  $socialMediaForm.addEventListener('submit', function (e) {
    e.preventDefault()
    const $websiteUrlInput = this.querySelector('[data-website-url]')
    const websiteUrlLabel = $websiteUrlInput.parentElement.parentElement.querySelector('.form__label').textContent
    const websiteUrlValue = $websiteUrlInput.value.trim() !== currentWebsiteUrl ? $websiteUrlInput.value.trim() : ''
    
    const $facebookUrlInput = this.querySelector('[data-facebook-url]')
    const facebookUrlLabel = $facebookUrlInput.parentElement.parentElement.querySelector('.form__label').textContent
    const facebookUrlValue = $facebookUrlInput.value.trim() !== currentFacebookUrl ? $facebookUrlInput.value.trim() : ''

    const $instagramUrlInput = this.querySelector('[data-instagram-url]')
    const instagramUrlLabel = $instagramUrlInput.parentElement.parentElement.querySelector('.form__label').textContent
    const instagramUrlValue = $instagramUrlInput.value.trim() !== currentInstagramUrl ? $instagramUrlInput.value.trim() : ''

    const $linkedinUrlInput = this.querySelector('[data-linkedin-url]')
    const linkedinUrlLabel = $linkedinUrlInput.parentElement.parentElement.querySelector('.form__label').textContent
    const linkedinUrlValue = $linkedinUrlInput.value.trim() !== currentLinkedinUrl ? $linkedinUrlInput.value.trim() : ''

    const data = {
      "website_url": [websiteUrlValue, "data-website-url", websiteUrlLabel],
      "facebook_url": [facebookUrlValue, "data-facebook-url", facebookUrlLabel],
      "instagram_url": [instagramUrlValue, "data-instagram-url", instagramUrlLabel],
      "linkedin_url": [linkedinUrlValue, "data-linkedin-url", linkedinUrlLabel],
    }

    if ( localizationSocialMediaSettingsClientValidation(data, $socialMediaForm) ) {
      socialMediaSettingsAjaxRequest(data)
    }
    
  })

}