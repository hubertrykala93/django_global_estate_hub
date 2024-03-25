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
   * Hero filters form
    */

const $heroForm = document.querySelector('[data-hero-form]')

if ($heroForm) {
  const $statusesParent = $heroForm.querySelector('[data-change-status]')
  const $locationParent = document.querySelector('[data-change-location]')
  const $categoriesParent = document.querySelector('[data-change-category]')
  const $yearsParent = document.querySelector('[data-change-year]')

  let currentlyChosenLocation = ''
  let currentlyChosenCategory = ''
  let currentlyChosenYear = ''
  
  const stopSubmitingWhenBotSends = function (e) {
    const urlValue = this.querySelector('.url').value
    if ( !urlValue == '' ) { e.preventDefault() }
  }

  const updateFilters = (response) => {
    //update location
    let newLocationsList = ''
    let locationNotInside = true
    response.chosenLocation.forEach(item => {
      if ( currentlyChosenLocation == item ) {
        locationNotInside = false
        newLocationsList += `
          <li role="option">
              <input data-option type="radio" value="${item}" id="${item}" name="location" checked>
              <label for="${item}">${item}</label>
          </li>
          `
      } else {
        newLocationsList += `
          <li role="option">
            <input data-option type="radio" value="${item}" id="${item}" name="location">
            <label for="${item}">${item}</label>
          </li>
          `
      }
    })
    if (locationNotInside) {
      $heroForm.querySelector('[data-selected-location]').innerText = 'Select Location'
      currentlyChosenLocation = ''
    }
    $locationParent.innerHTML = newLocationsList

    //update categories
    let newCategoriesList = ''
    let categoryNotInside = true
    response.chosenCategory.forEach(item => {
        if ( currentlyChosenCategory == item ) {
          categoryNotInside = false
          newCategoriesList += `
            <li role="option">
              <input data-option type="radio" value="${item}" id="${item}" name="category" checked>
              <label for="${item}">${item}</label>
            </li>
          `
        } else {
          newCategoriesList += `
            <li role="option">
              <input data-option type="radio" value="${item}" id="${item}" name="category">
              <label for="${item}">${item}</label>
            </li>
          `
        }
    })
    if (categoryNotInside) {
      $heroForm.querySelector('[data-selected-category]').innerText = 'Select Property Type'
      currentlyChosenCategory = ''
    }
    $categoriesParent.innerHTML = newCategoriesList

    //update years
    let newYearsList = ''
    let yearNotInside = true
    response.chosenYear.forEach(item => {
      if ( currentlyChosenYear == item ) {
          yearNotInside = false
          newYearsList += `
            <li role="option">
              <input data-option type="radio" value="${item}" id="${item}" name="year" checked>
              <label for="${item}">${item}</label>
            </li>
          `
        } else {
          newYearsList += `
            <li role="option">
              <input data-option type="radio" value="${item}" id="${item}" name="year">
              <label for="${item}">${item}</label>
            </li>
          `
        }
    })
    if (yearNotInside) {
      $heroForm.querySelector('[data-selected-year]').innerText = 'Select year'
      currentlyChosenYear = ''
    }
    $yearsParent.innerHTML = newYearsList
  }

  $heroForm.addEventListener('submit', stopSubmitingWhenBotSends)

  $heroForm.addEventListener('change', (e) => {
    const data = {}

    //status
    let chosenStatus = ''
    const $statusesInputs = $statusesParent.querySelectorAll('[data-input]')
    for (let i = 0; i < $statusesInputs.length; i++) {
        if ( $statusesInputs[i].checked ) {
            chosenStatus = $statusesInputs[i].value
        }
    }
    data.chosenStatus = chosenStatus

    //location
    const $locationInputs = $locationParent.querySelectorAll('[data-option]')
    for (let i = 0; i < $locationInputs.length; i++) {
        if ( $locationInputs[i].checked ) {
          currentlyChosenLocation = $locationInputs[i].value
        }
    }
    data.chosenLocation = currentlyChosenLocation

    //category
    const $categoriesInputs = $categoriesParent.querySelectorAll('[data-option]')
    for (let i = 0; i < $categoriesInputs.length; i++) {
        if ( $categoriesInputs[i].checked ) {
          currentlyChosenCategory = $categoriesInputs[i].value
        }
    }
    data.chosenCategory = currentlyChosenCategory

    //year
    const $yearsInputs = $yearsParent.querySelectorAll('[data-option]')
    for (let i = 0; i < $yearsInputs.length; i++) {
        if ( $yearsInputs[i].checked ) {
          currentlyChosenYear = $yearsInputs[i].value
        }
    }
    data.chosenYear = currentlyChosenYear

    const xhr = new XMLHttpRequest()
    xhr.open('POST', 'properties-results', true)
    xhr.setRequestHeader('X-CSRFToken', csrfToken)
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    xhr.send(JSON.stringify(data))

    xhr.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
          const response = JSON.parse(this.responseText)
          updateFilters(response)
      }
    }
  })
}

/**
   * Hero counters
    */

const $heroCounters = document.querySelector('[data-hero-counters]')

if ($heroCounters) {
  
  const countNumbers = () => {
    const DURATION = 3000
    const INCREMENT_VALUE = 1
    const $counters = $heroCounters.querySelectorAll('[data-number]')

    $counters.forEach(counter => {
      const targetNumber = counter.dataset.number
      const interval = DURATION / targetNumber
      let number = 0

      counter.innerText = number

      const loop = setInterval(() => {
        number+= INCREMENT_VALUE
        counter.innerText = number

        if ( number >= targetNumber ) {
          counter.innerText = targetNumber
          clearInterval(loop)
        }
      }, interval);
    })
  }

  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        countNumbers()
        obs.unobserve(entry.target)
      }
    })
  })

  observer.observe($heroCounters)
}


/**
   * Categories carousel
    */

$categoriesSection = document.querySelector('[data-home-categories]')

if ($categoriesSection) {
  const $categoriesCarousel = $categoriesSection.querySelector('[data-home-categories-carousel]')

  const swiper = new Swiper($categoriesCarousel, {
    navigation: {
      nextEl:  $categoriesSection.querySelector('[data-right]'),
      prevEl: $categoriesSection.querySelector('[data-left]'),
    },
    draggable: true,
    speed: 400,
    slidesPerView: 1,
    spaceBetween: 24,
    breakpoints: {
      640: {
        slidesPerView: 2,
      },
      992: {
        slidesPerView: 3,
      },
      1200: {
        slidesPerView: 4,
      }
    },
  })
}

/**
   * Cities carousel
    */

$citiesSection = document.querySelector('[data-home-cities]')

if ($citiesSection) {
  const $citiesCarousel = $citiesSection.querySelector('[data-home-cities-carousel]')

  const swiper = new Swiper($citiesCarousel, {
    navigation: {
      nextEl:  $citiesSection.querySelector('[data-right]'),
      prevEl: $citiesSection.querySelector('[data-left]'),
    },
    draggable: true,
    speed: 400,
    slidesPerView: 1,
    spaceBetween: 24,
    breakpoints: {
      640: {
        slidesPerView: 2,
      },
      992: {
        slidesPerView: 3,
      },
      1200: {
        slidesPerView: 4,
      }
    },
  })
}

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
  const $messageNode = form.querySelector(`[${field}]`).closest('.form__field').querySelector('.info')
  if ($messageNode) { $messageNode.remove() }
}

const showInfo = (isValid, message, $form, field)=> {
  const $inputParentField = $form.querySelector(`[${field}]`).closest('.form__field')
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
    if ( field !== 'data-gender' ) { $form.querySelector(`[${field}]`).value = "" }
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
      if ( input.type !== 'checkbox' && input.type !== 'radio' ) {
        input.value = ''
      }
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

const getRadioValue = (form, radioDataAttr) => {
  const radios = form.querySelectorAll(`[${radioDataAttr}]`)

  for (let i = 0; i < radios.length; i++) {
    if(radios[i].checked === true) {
      return radios[i].value
    }
  }
  return ''
}

const decodeCommentIntoText = (comment) => {
  return decodeURIComponent(comment).replace(/\n/g, '<br>').replace(/\s/g, ' ')
}

/**
   * Custom select element
    */

const $customSelects = document.querySelectorAll('[data-custom-select]')

if ( $customSelects.length ) {
  const toggleSelect = ($select, $btn) => {
      $select.classList.toggle('active')

      $btn.setAttribute(
        'aria-expanded',
        $btn.getAttribute('aria-expanded') === 'true' ? 'false' : 'true'
      )
  }

  const closeSelect = ($select, $btn) => {
    $select.classList.remove('active')

    $btn.setAttribute('aria-expanded', 'false')
  }

  const closeAllSelects = () => {
    const $activeSelects = document.querySelectorAll('[data-custom-select].active')
    if ( $activeSelects.length ) {
      $activeSelects.forEach(select => {
        const $selectBtn = select.querySelector('[data-custom-select-btn]')
        closeSelect(select, $selectBtn)
      })
    }
  }

  $customSelects.forEach(select => {
    const $selectBtn = select.querySelector('[data-custom-select-btn]')

    $selectBtn.addEventListener('click', () => {
      // closeAllSelects()

      toggleSelect(select, $selectBtn)
    })

    select.addEventListener('click', e => {
      if ( e.target.tagName === 'INPUT' ) {
        const $btnValue = $selectBtn.querySelector('[data-custom-select-btn-value]')
        closeSelect(select, $selectBtn)

        $btnValue.textContent = e.target.value
      }
    })
  })

  // if esc key was not pressed in combination with ctrl or alt or shift
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        const isNotCombinedKey = !(e.ctrlKey || e.altKey || e.shiftKey);
        if (isNotCombinedKey) {
          closeAllSelects()
        }
    }
  })

}

/**
   * Custom range slider
    */

const $rangeSliderWrapper = document.querySelector('[data-range-slider]')

if ( $rangeSliderWrapper ) {
  const minGap = 0

  const slideMin = () => {
    const $minValue = $rangeSliderWrapper.querySelector('[data-range-min-input]')
    const $maxValue = $rangeSliderWrapper.querySelector('[data-range-max-input]')
    const $minBox = $rangeSliderWrapper.querySelector('[data-range-min-box]')

    let gap = parseInt($maxValue.value) - parseInt($minValue.value)
    if ( gap <= minGap ) {
      $minValue.value = parseInt($maxValue.value) - minGap
    }
    $minBox.textContent = $minValue.value
    setRangeSize()
  }

  const slideMax = () => {
    const $minValue = $rangeSliderWrapper.querySelector('[data-range-min-input]')
    const $maxValue = $rangeSliderWrapper.querySelector('[data-range-max-input]')
    const $maxBox = $rangeSliderWrapper.querySelector('[data-range-max-box]')

    let gap = parseInt($maxValue.value) - parseInt($minValue.value)
    if ( gap <= minGap ) {
      $maxValue.value = parseInt($minValue.value) - minGap
    }
    $maxBox.textContent = $maxValue.value
    setRangeSize()
  }

  const setRangeSize = () => {
    const $minValue = $rangeSliderWrapper.querySelector('[data-range-min-input]')
    const $maxValue = $rangeSliderWrapper.querySelector('[data-range-max-input]')
    const $track = $rangeSliderWrapper.querySelector('[data-range-slider-track]')
    const sliderMinValue = parseInt($minValue.min)
    const sliderMaxValue = parseInt($minValue.max)

    $track.style.left = `${($minValue.value - sliderMinValue) / (sliderMaxValue - sliderMinValue) * 100}%`
    $track.style.right = `${100 - (($maxValue.value - sliderMinValue) / (sliderMaxValue - sliderMinValue)) * 100}%`
  }

  slideMin()
  slideMax()
  setRangeSize()

  const $minValue = $rangeSliderWrapper.querySelector('[data-range-min-input]')
  const $maxValue = $rangeSliderWrapper.querySelector('[data-range-max-input]')

  $minValue.addEventListener('input', () => {
    slideMin()
  })
  $maxValue.addEventListener('input', () => {
    slideMax()
  })
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

    if ( data.email == '' ) {
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

  $newsletterForm.addEventListener('submit', function(e) {
    e.preventDefault()
    const urlValue = this.querySelector('[name="url"]').value
    if ( !urlValue == '' ) { return false }

    const $emailInput = $newsletterForm.querySelector('[data-email]')
    const data = {
      "email": $emailInput.value.trim(),
      "url": urlValue
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
        eye.classList.add('ri-eye-line')
        eye.classList.remove('ri-eye-off-line')
      } else{
        $input.type = 'password'
        eye.classList.add('ri-eye-off-line')
        eye.classList.remove('ri-eye-line')
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


/**
  * Contact us form
   */

const $contactUsForm = document.querySelector('[data-contact-form]')

if ($contactUsForm) {

  const ajaxRequest = (data)=>{
    const xhr = new XMLHttpRequest()

    xhr.open('POST', 'send-message', true)
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
    const urlValue = this.querySelector('[name="url"]').value
    if ( !urlValue == '' ) { return false }

    const $fullNameInput = this.querySelector('[data-fullname]')
    const $fullNameLabel = $fullNameInput.parentElement.parentElement.querySelector('label').textContent
    const $phoneInput = this.querySelector('[data-phone]')
    const $phoneLabel = $phoneInput.parentElement.parentElement.querySelector('label').textContent
    const $emailInput = this.querySelector('[data-email]')
    const $emailLabel = $emailInput.parentElement.parentElement.querySelector('label').textContent
    const $contentInput = this.querySelector('[data-content]')
    const $contentLabel = $contentInput.parentElement.parentElement.querySelector('label').textContent

    const data = {
      "fullName": [$fullNameInput.value.trim(), 'data-fullname', $fullNameLabel],
      "phone": [$phoneInput.value.trim(), 'data-phone', $phoneLabel],
      "email": [$emailInput.value.trim(), 'data-email', $emailLabel],
      "content": [$contentInput.value.trim(), 'data-content', $contentLabel],
      "url": urlValue,
    }
    
    if( clientValidation($contactUsForm, data) ) {
      ajaxRequest(data)
    }
  })
}


/*----------------------------------*\
  #ARTICLES COMMENTS CRUD
\*----------------------------------*/

const $articlesCommentsWrapper = document.querySelector('[data-article-comments]')

if ( $articlesCommentsWrapper ) {
  const $commentsCounter = $articlesCommentsWrapper.querySelector('[data-comments-counter]')
  let url = window.location.pathname
  url = url.slice(url.lastIndexOf('/') + 1)

  const updateLikesAndDislikes = (action, response)=> {
    const $comment = $articlesCommentsWrapper.querySelector(`[data-comment-id="${response.commentId}"]`)
    const $likesCounter = $comment.querySelector('[data-comment-likes-counter]')
    const $dislikesCounter = $comment.querySelector('[data-comment-dislikes-counter]')
    const $likesIcon = $comment.querySelector('[data-comment-like-btn] i')
    const $dislikesIcon = $comment.querySelector('[data-comment-dislike-btn] i')

    if ( action === 'like') {
      $dislikesIcon.classList.add('ri-thumb-down-line')
      $dislikesIcon.classList.remove('ri-thumb-down-fill')
      if ( response.valid === true ) {
        $likesIcon.classList.remove('ri-thumb-up-line')
        $likesIcon.classList.add('ri-thumb-up-fill')
      } else {
        $likesIcon.classList.add('ri-thumb-up-line')
        $likesIcon.classList.remove('ri-thumb-up-fill')
      }
    } else if ( action === 'dislike' ) {
        $likesIcon.classList.add('ri-thumb-up-line')
        $likesIcon.classList.remove('ri-thumb-up-fill')
        if ( response.valid === true ) {
          $dislikesIcon.classList.remove('ri-thumb-down-line')
          $dislikesIcon.classList.add('ri-thumb-down-fill')
        } else {
          $dislikesIcon.classList.add('ri-thumb-down-line')
          $dislikesIcon.classList.remove('ri-thumb-down-fill')
        }
      }

    $likesCounter.textContent = response.likes
    $dislikesCounter.textContent = response.dislikes

  }

  const likesHandler = (btn)=>{
    const commentId = btn.closest('[data-article-comment]').dataset.commentId

    const data = {
      commentId
    }
    
    const xhr = new XMLHttpRequest()
    xhr.open('PUT', url + '/give-like', true)
    xhr.setRequestHeader('X-CSRFToken', csrfToken)
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    xhr.send(JSON.stringify(data))

    xhr.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
          const response = JSON.parse(this.responseText)
          updateLikesAndDislikes('like', response)
      }
    }
  }

  const dislikesHandler = (btn)=>{
    const commentId = btn.closest('[data-article-comment]').dataset.commentId

    const data = {
      commentId
    }

    const xhr = new XMLHttpRequest()
    xhr.open('PUT', url + '/give-dislike', true)
    xhr.setRequestHeader('X-CSRFToken', csrfToken)
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    xhr.send(JSON.stringify(data))

    xhr.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
          const response = JSON.parse(this.responseText)
          updateLikesAndDislikes('dislike', response)
      }
    }
  }

  const deleteComment = (response) => {
    const $comment = $articlesCommentsWrapper.querySelector(`[data-comment-id="${response.commentId}"]`)
    if ( response.valid ) {
      $comment.remove()
      $commentsCounter.textContent = response.commentsCounter
    } else {
      const $error = $comment.querySelector('.article__comment__error')
      if($error) {
        $error.textContent = response.message
      } else {
        const newError = document.createElement('div')
        newError.classList.add('article__comment__error')
        newError.textContent = response.message
        $comment.appendChild(newError)
      }
    }
  }

  const deleteHandler = (btn) => {
    const commentId = btn.closest('[data-article-comment]').dataset.commentId
    
    const data = {
      commentId
    }

    const xhr = new XMLHttpRequest()
    xhr.open('DELETE', url + '/delete-comment', true)
    xhr.setRequestHeader('X-CSRFToken', csrfToken)
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    xhr.send(JSON.stringify(data))

    xhr.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
          const response = JSON.parse(this.responseText)
          deleteComment(response)
      }
    }
  }

  const editHandler = (btn) => {
    const commentId = btn.closest('[data-article-comment]').dataset.commentId
    const $comment = $articlesCommentsWrapper.querySelector(`[data-comment-id="${commentId}"]`)
    let oldContent = $comment.querySelector('[data-comment-content-body]').textContent.trim()
    const $replyForm = $articlesCommentsWrapper.querySelector('.article__comment__reply__form')
    if ($replyForm ) { $replyForm.remove() }

    if ( !$comment.querySelector('.article__comment__edit__form') ) {
      let editForm = document.createElement('div')
      editForm.classList.add('article__comment__edit__form')
      editForm.innerHTML = `
      <form data-article-comment-edit class="theme-form">

      <div style="opacity: 0; position: absolute; top: 0; left: 0; height: 0; width: 0; z-index: -1;">
        <label>leave this field blank to prove your humanity
            <input type="text" name="url" value="" autocomplete="off">
        </label>
      </div>
  
        <div class="form__row">
            <div class="form__field">
                <div class="form__input-wrap">
                    <textarea data-comment data-input placeholder="Write new content here...">${oldContent}</textarea>
                </div>
            </div>
        </div>
  
        <div class="form__row submit-row">
            <div class="form__field form__submit">
                <button class="btn secondary-btn btn--auto-width" type="submit">Apply changes</button>
            </div>
        </div>
      </form>
      `
      $comment.append(editForm)
    }

    const $editForm = $comment.querySelector('[data-article-comment-edit]')
    
    const serverResponse = (response) => {
      if ( response.valid ) {
        const $commentContent = $comment.querySelector('[data-comment-content-body]')
        $commentContent.innerHTML = response.newContent
        $comment.querySelector('.article__comment__edit__form').remove()
      } else {
        showInfo(false, response.message, $editForm, 'data-comment')
      }

    }

    const ajaxRequest = (data)=>{
      const xhr = new XMLHttpRequest()
      xhr.open('PATCH', url + '/edit-comment', true)
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
    
    $editForm.addEventListener('submit', function (e) {
      e.preventDefault()
      const $commentInput = this.querySelector('[data-comment]')
      const $urlInput = this.querySelector('[name="url"]')
  
      const data = {
        "commentId": commentId,
        "comment": [$commentInput.value.trim(), "data-comment", "comment"],
        "url": $urlInput.value,
      }

       if ( $commentInput.value.trim() !== oldContent ) {
         if ( clientValidation($editForm, data) ) {
           ajaxRequest(data)
         }
       } else {
        showInfo(false, 'The comment was not edited correctly because its content did not change.', $editForm, 'data-comment')
       }
    })
  }

  const replyHandler = (btn) => {
    const commentId = btn.closest('[data-article-comment]').dataset.commentId
    const $comment = $articlesCommentsWrapper.querySelector(`[data-comment-id="${commentId}"]`)
    const $editForm = $articlesCommentsWrapper.querySelector('.article__comment__edit__form')
    if ($editForm ) { $editForm.remove() }

    if ( !$comment.querySelector('.article__comment__reply__form') ) {
      let replyForm = document.createElement('div')
      replyForm.classList.add('article__comment__reply__form')
      let nameInputHtml = ''
      if ( loggedIn ) {
        nameInputHtml = `<input data-name data-input type="text" value="${userName}" placeholder="Name" disabled aria-hidden="true">`
      } else {
        nameInputHtml = `<input data-name data-input type="text" placeholder="Name">`
      }
      replyForm.innerHTML = `
      <form data-article-comment-reply class="theme-form">

      <div style="opacity: 0; position: absolute; top: 0; left: 0; height: 0; width: 0; z-index: -1;">
          <label>leave this field blank to prove your humanity
              <input type="text" name="url" value="" autocomplete="off" tabindex="-1">
          </label>
      </div>

      <div class="form__row">
        <div class="form__field">
            <div class="form__input-wrap">
                ${nameInputHtml}
            </div>
        </div>
      </div>

      <div class="form__row">
        <div class="form__field">
            <div class="form__input-wrap">
                <textarea data-comment data-input placeholder="Write your comment here..." aria-label="Write your comment here"></textarea>
            </div>
        </div>
      </div>

        <div class="form__row submit-row">
            <div class="form__field form__submit">
                <button class="btn secondary-btn btn--auto-width" type="submit">Reply for comment</button>
            </div>
        </div>
      </form>
      `
      $comment.append(replyForm)
    }

    const $replyForm = $comment.querySelector('[data-article-comment-reply]')

    const serverResponse = (response)=> {
    if ( response.valid === null ) {
      return false
    } else if ( response.valid === true ) {
      $replyForm.querySelectorAll('[data-input]').forEach(input =>{
        if (  !input.disabled ) {
          input.value = ''
        }

        const $messageNode = input.closest('.form__field').querySelector('.info')
        if ($messageNode) { $messageNode.remove() }
      })

      successfullySentMessage($replyForm, response.message, true)
    } else {
      response.forEach(item => {
        if ( !item.valid ) {
          showInfo(item.valid, item.message, $replyForm, item.field)
        } else {
          removeInfo($replyForm, item.field)
        }
      })
    }
  }

    const ajaxRequest = (data)=>{
      const xhr = new XMLHttpRequest()
      xhr.open('POST', url + '/reply-comment', true)
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

    $replyForm.addEventListener('submit', function (e) {
      e.preventDefault()
      const urlValue = this.querySelector('[name="url"]').value
      if ( !urlValue == '' ) { return false }

      const $nameInput = this.querySelector('[data-name]')
      const $commentInput = this.querySelector('[data-comment]')

      const data = {
        "comment_id": commentId,
        "full_name": [$nameInput.value.trim(), "data-name", "name"],
        "comment": [$commentInput.value.trim(), "data-comment", "comment"],
        "url": urlValue,
      }

      if ( clientValidation($replyForm, data) ) {
         ajaxRequest(data)
      }
    })

  }

  $articlesCommentsWrapper.addEventListener('click', (e) => {
    //likes
    if (e.target.matches('[data-comment-like-btn], [data-comment-like-btn] *')) {
      likesHandler(e.target)
    }
    //dislikes
    else if (e.target.matches('[data-comment-dislike-btn], [data-comment-dislike-btn] *')) {
      dislikesHandler(e.target)
    }
    //delete
    else if (e.target.matches('[data-comment-delete-btn], [data-comment-delete-btn] *')) {
      deleteHandler(e.target)
    }
    //edit
    else if (e.target.matches('[data-comment-edit-btn], [data-comment-edit-btn] *')) {
      editHandler(e.target)
    }
    //reply
    else if (e.target.matches('[data-comment-reply-btn], [data-comment-reply-btn] *')) {
      replyHandler(e.target)
    }
  })

  //comments decode with white spaces
  const $allComments = $articlesCommentsWrapper.querySelectorAll('[data-comment-content-body]')

  if($allComments.length) {
    $allComments.forEach(comment => {
      comment.innerHTML = decodeCommentIntoText(comment.innerHTML.trim())
    })
  }
}


/**
  * Article add comment form
   */

const $addCommentInArticleForm = document.querySelector('[data-article-comment-form]')

if ($addCommentInArticleForm) {

  let url = window.location.pathname
  url = url.slice(url.lastIndexOf('/') + 1)

  const serverResponse = (response)=> {
    if ( response.valid === null ) {
      return false
    } else if ( response.valid === true ) {

      $addCommentInArticleForm.querySelectorAll('[data-input]').forEach(input =>{
        if (  !input.disabled ) {
          input.value = ''
        }

        const $messageNode = input.closest('.form__field').querySelector('.info')
        if ($messageNode) { $messageNode.remove() }
      })

      successfullySentMessage($addCommentInArticleForm, response.message, true)
    } else {
      response.forEach(item => {
        if ( !item.valid ) {
          showInfo(item.valid, item.message, $addCommentInArticleForm, item.field)
        } else {
          removeInfo($addCommentInArticleForm, item.field)
        }
      })
    }
  }

  const ajaxRequest = (data)=>{
    const xhr = new XMLHttpRequest()
    xhr.open('POST', url + '/add-comment', true)
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
  
  $addCommentInArticleForm.addEventListener('submit', function (e) {
    e.preventDefault()
    const urlValue = this.querySelector('[name="url"]').value
    if ( !urlValue == '' ) { return false }

    const $nameInput = this.querySelector('[data-name]')
    const $commentInput = this.querySelector('[data-comment]')

    const data = {
      "full_name": [$nameInput.value.trim(), "data-name", "name"],
      "comment": [encodeURI($commentInput.value.trim()), "data-comment", "comment"],
      "url": urlValue
    }

    if ( clientValidation($addCommentInArticleForm, data) ) {
      ajaxRequest(data)
    }

  })
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


/*----------------------------------*\
  #PROPERTIES
\*----------------------------------*/

const $propertiesPage = document.querySelector('[data-properties]')

if ( $propertiesPage ) {
  const $propertiesRow = $propertiesPage.querySelector('[data-properties-row]')
  const $filtersForm = $propertiesPage.querySelector('[data-properties-filters-form]')

  /**
   * Change view
    */

  const $changeView = $propertiesPage.querySelector('[data-change-view]')
  const $gridBtn = $propertiesPage.querySelector('[data-grid-btn]')
  const $listBtn = $propertiesPage.querySelector('[data-list-btn]')
  const view = localStorage.getItem('view') || 'grid'

  const changeView = (view) => {
    if ( view === 'grid' ) {
      $propertiesRow.classList.remove('properties-cards__row--list')
      $propertiesRow.classList.add('properties-cards__row--grid')
      $listBtn.classList.remove('active')
      $gridBtn.classList.add('active')
    } else if ( view === 'list' ) {
      $propertiesRow.classList.remove('properties-cards__row--grid')
      $propertiesRow.classList.add('properties-cards__row--list')
      $gridBtn.classList.remove('active')
      $listBtn.classList.add('active')
    }
  }

  if ($propertiesRow) { changeView(view) }

  $changeView.addEventListener('click', e => {
    if ( e.target.dataset.hasOwnProperty('gridBtn') ) {
      changeView('grid')
      localStorage.setItem('view', 'grid')
    } else if ( e.target.dataset.hasOwnProperty('listBtn') ) {
      changeView('list')
      localStorage.setItem('view', 'list')
    }
  })

  /**
   * Add to favourite
    */

  const addToFavouritesHandler = ($btn) => {
    const propertyId = $btn.closest('.property-card__wrapper').dataset.id

    const serverResponse = (response) => {
      if ( response.valid ) {
        const $favouritesBtn = $propertiesPage.querySelector(`[data-property-card][data-id="${response.propertyId}"]`).querySelector('[data-add-to-favourites]')
        $favouritesBtn.classList.toggle('active')
      }
    }

    const data = {
      propertyId
    }

    const xhr = new XMLHttpRequest()
  
    xhr.open('PATCH', 'add-to-favourites', true)
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

  $propertiesRow?.addEventListener('click', e=> {
    // add to favourites
    if ( e.target.dataset.hasOwnProperty('addToFavourites') ) {
      addToFavouritesHandler(e.target)
    }
  })

  /**
   * Prevent filter forms submit when bot is sending
    */

  const $searchForm = $propertiesPage.querySelector('[data-properties-search-form]')
  
  const stopSubmitingWhenBotSends = function (e) {
    const urlValue = this.querySelector('.url').value
    if ( !urlValue == '' ) { e.preventDefault() }
  }

  $searchForm?.addEventListener('submit', stopSubmitingWhenBotSends)
  $filtersForm?.addEventListener('submit', stopSubmitingWhenBotSends)

  /**
   * Updating filers form
    */

  $filtersForm?.addEventListener('change', function(e) {
      this.submit()
  })
}


/*----------------------------------*\
  #PROPERTY DETAILS
\*----------------------------------*/

const $propertyPage = document.querySelector('[data-property]')

if ($propertyPage) {

  let url = window.location.pathname
  url = url.slice(url.lastIndexOf('/') + 1)

  /**
   * Nearby tabs
    */

  const $nearbyWrapper = $propertyPage.querySelector('[data-property-nearby]')
  if ($nearbyWrapper) {
    const $contents = $nearbyWrapper.querySelectorAll('[data-property-nearby-content]')

    $nearbyWrapper.addEventListener('click', e => {
      if ( e.target.matches('[data-property-nearby-button], [data-property-nearby-button] *') ) {
        const currentBtn = e.target.dataset.hasOwnProperty('propertyNearbyButton') ? e.target : e.target.closest('[data-property-nearby-button]')
        let currentId = +currentBtn.dataset.id
        $nearbyWrapper.querySelector('[data-property-nearby-button].active').classList.remove('active')
        currentBtn.classList.add('active')

        $contents.forEach((content, index) => {
          if (index === currentId - 1) {
            content.classList.add('active')
          } else {
            content.classList.remove('active')
          }
        })
      }
    })
  }

  /**
   * Schedule A Tour
    */

  const $scheduleForm = $propertyPage.querySelector('[data-property-schedule-form]')

  if ($scheduleForm) {

    const serverResponse = (response)=> {
      if ( response.valid === null ) {
        return false
      } else if ( response.valid === true ) {
  
        $scheduleForm.querySelectorAll('[data-input]').forEach(input =>{
          if (  !input.disabled ) {
            input.value = ''
          }
  
          const $messageNode = input.closest('.form__field').querySelector('.info')
          if ($messageNode) { $messageNode.remove() }
        })
  
        successfullySentMessage($scheduleForm, response.message, true)
      } else if ( response.valid === false ) {
        successfullySentMessage($scheduleForm, response.message, true)
      }
      else {
        response.forEach(item => {
          if ( !item.valid ) {
            showInfo(item.valid, item.message, $scheduleForm, item.field)
          } else {
            removeInfo($scheduleForm, item.field)
          }
        })
      }
    }

    const ajaxRequest = (data)=>{
      const xhr = new XMLHttpRequest()
      xhr.open('POST', url + '/schedule-tour', true)
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

    const clientValidation = (form, data) => {
      let isAllValid = true
    
      const regexValidation = (form, field, value) => {
        const phoneRegex = /^\+?[1-9][0-9]{7,14}$/
    
        if ( field === 'data-phone' ) {
          if ( !phoneRegex.test(value) ) {
            showInfo(false, `The ${data.phone[2]} format is invalid.`, form, field)
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
          if (key == 'name' || key == 'message') { return false }
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

    $scheduleForm.addEventListener('submit', function (e) {
      e.preventDefault()
      const urlValue = this.querySelector('[name="url"]').value
      if ( !urlValue == '' ) { return false }
  
      const $dateInput = this.querySelector('[data-date]')

      const $timeInputs = [...this.querySelectorAll('[name="time"]')]
      const chosenTime = $timeInputs.find(el => el.checked).value

      const $nameInput = this.querySelector('[data-name]')
      const $phoneInput = this.querySelector('[data-phone]')
      const $messageInput = this.querySelector('[data-message]')
  
      const data = {
        "date": [$dateInput.value.trim(), 'data-date', 'date'],
        "time": [chosenTime, 'name="time"', 'time'],
        "name": [$nameInput.value.trim(), 'data-name', 'name'],
        "phone": [$phoneInput.value.trim(), 'data-phone', 'phone'],
        "message": [$messageInput.value.trim(), 'data-message', 'message'],
        "url": urlValue
      }
      
      if ( clientValidation($scheduleForm, data) ) {
        ajaxRequest(data)
      }
    })
  }

  /**
   * Mortgage Calculator
    */

  const mortgageStats = {
    $barsWrapper: $propertyPage.querySelector('[data-mortgage-bars]'),
    $stat1: $propertyPage.querySelector('[data-stat1]'),
    $stat2: $propertyPage.querySelector('[data-stat2]'),
    $stat3: $propertyPage.querySelector('[data-stat3]'),
    numberWithCommas: function (num) {
      return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    },
    updateBars: function (p1, p2, p3) {
      this.$barsWrapper.style.gridTemplateColumns = `${p1}% ${p2}% ${p3}%`
    },
    updateStats: function (s1, s2, s3) {
      this.$stat1.innerText = this.numberWithCommas(s1)
      this.$stat2.innerText = this.numberWithCommas(s2)
      this.$stat3.innerText = this.numberWithCommas(s3)
    }
  }

  const mortgageCalculator = {
    form: $propertyPage.querySelector('[data-mortgage-form]'),
    calculate: function (elements) {
      const totalAmount = Number(elements['total-amount'].value)
      const downPayment = Number(elements['down-payment'].value) || 0
      const interestRate = Number(elements['interest-rate'].value)
      const loanTerms = Number(elements['loan-terms'].value)
      const propertyTax = Number(elements['property-tax'].value) || 0
      const homeInsurance = Number(elements['home-insurance'].value) || 0

      const tax = ((totalAmount * propertyTax) / 100) * loanTerms
      const loanValue = totalAmount - downPayment
      const agentCommission = totalAmount * 0.005
      const loanInterest = (loanValue * interestRate) / 100 + tax + (homeInsurance * loanTerms) + agentCommission
      const fullAmount = totalAmount + loanInterest

      const bankPayment = loanValue
      const bankPercent = (bankPayment * 100) / fullAmount
      const userPayment = downPayment
      const userPercent = (userPayment * 100) / fullAmount
      const restPayment = fullAmount - loanValue - downPayment
      const restPercent = (restPayment * 100) / fullAmount
      
      mortgageStats.updateBars(bankPercent, userPercent, restPercent)
      mortgageStats.updateStats(bankPayment, userPayment, restPayment)
    },
    liveValidation: function (e) {
      const input = e.target
      const value = input.value.trim()
      const inputName = input.name
      let cutValue = value

      if ( Number(isNaN(value)) ) {
        cutValue = value.substring(0, value.length - 1)
        if ( Number(isNaN(cutValue)) ) {
          while ( Number(isNaN(cutValue)) && cutValue.length ) {
            cutValue = cutValue.substring(0, cutValue.length - 1)
          }
        }
        input.value = cutValue
      }
      if ( Number(cutValue[0]) === 0 ) {
        input.value = cutValue.substring(0, 0)
      }
    },
    validation: function (e) {
      e.preventDefault()
      let isValid = true
      const $elements = [...mortgageCalculator.form.elements].filter(item => item.nodeName === 'INPUT')

      $elements.forEach(input => {
        const value = Number(input.value)
        if (value == '' && input.dataset.hasOwnProperty('required')) {
          showInfo(false, 'Field cannot be empty', mortgageCalculator.form, `name="${input.name}"`)
          isValid = false
        } else if ( value < 0 ) {
          showInfo(false, 'Value cannot be less than 0', mortgageCalculator.form, `name="${input.name}"`)
          isValid = false
        }
        else {
          removeInfo(mortgageCalculator.form, `name="${input.name}"`)
        }
      })

      if (isValid) {
        mortgageCalculator.calculate(mortgageCalculator.form.elements)
      }
    },
  }

  mortgageCalculator.form.addEventListener('submit', mortgageCalculator.validation)
  mortgageCalculator.form.addEventListener('input', mortgageCalculator.liveValidation)


  /**
   * Add review
    */

  const $addReviewForm = $propertyPage.querySelector('[data-property-review-form]')

  if ($addReviewForm) {

    const serverResponse = (response)=> {
      if ( response.valid === null ) {
        return false
      } else if ( response.valid === true ) {
  
        $addReviewForm.querySelectorAll('[data-input]').forEach(input =>{
          if (  !input.disabled ) {
            input.value = ''
          }
  
          const $messageNode = input.closest('.form__field').querySelector('.info')
          if ($messageNode) { $messageNode.remove() }
        })
  
        successfullySentMessage($addReviewForm, response.message, true)
      } else {
        response.forEach(item => {
          if ( !item.valid ) {
            showInfo(item.valid, item.message, $addReviewForm, item.field)
          } else {
            removeInfo($addReviewForm, item.field)
          }
        })
      }
    }

    const ajaxRequest = (data)=>{
      const xhr = new XMLHttpRequest()
      xhr.open('POST', url + '/add-review', true)
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

    $addReviewForm.addEventListener('submit', function (e) {
      e.preventDefault()
      const urlValue = this.querySelector('[name="url"]').value
      if ( !urlValue == '' ) { return false }
  
      const $rateInputs = [...this.querySelectorAll('[data-star]')]
      const chosenRate = $rateInputs.find(el => el.checked).value
      const $commentInput = this.querySelector('[data-comment]')
  
      const data = {
        "rate": [chosenRate, "data-star", "rating"],
        "comment": [encodeURI($commentInput.value.trim()), "data-comment", "comment"],
        "url": urlValue
      }

      
      if ( clientValidation($addReviewForm, data) ) {
        ajaxRequest(data)
      }
  
    })
  }
  
  /**
   * Comments decode with white spaces
    */
  
  const $allComments = $propertyPage.querySelectorAll('[data-property-review-text]')

  if($allComments.length) {
    $allComments.forEach(comment => {
      comment.innerHTML = decodeCommentIntoText(comment.innerHTML.trim())
    })
  }
}