/*----------------------------------*\
  #FORMS
\*----------------------------------*/

/**
   * Forms reusable functions
    */

/**
 * Removes message from a particular input in form
 * @param {HTMLElement} form - form element where you want to remove info message
 * @param {string} field - data selector of nearest input
 */
const removeInfo = (form, field)=>{
  const $messageNode = form.querySelector(`[${field}]`).closest('.form__field').querySelector('.info')
  if ($messageNode) { $messageNode.remove() }
}

/**
 * Shows message to a particular input in form
 * @param {boolean} isValid - is error or success message
 * @param {string} message - content of message
 * @param {HTMLElement} $form - form element where you want to add info message
 * @param {string} field - data selector of input under which you want to place the message
 */
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

/**
 * Validates form input values before sending with Ajax
 * @param {HTMLElement} form - form element where you want to valid inputs
 * @param {Object} data - set of inputs values
 * @returns {boolean} - true if all valid / false if anything invalid 
 */
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

/**
 * Clears all inputs values in form
 * @param {HTMLElement} form - form element where you want to clear inputs
 */
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

/**
 * Shows message under form when it is submited correctly
 * @param {HTMLElement} form - form element under which you want to show message
 * @param {string} message - message to show
 * @param {boolean} hide - if true message disappear after 2000 miliseconds
 */
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

/**
 * Returns value of checked radio element in form
 * @param {HTMLElement} form - form element where radio elements are placed
 * @param {string} radioDataAttr - data selector of radio set to get
 * @returns {string} - if checked radio element is found it returns its value, if not - returns empty string
 */
const getRadioValue = (form, radioDataAttr) => {
  const radios = form.querySelectorAll(`[${radioDataAttr}]`)

  for (let i = 0; i < radios.length; i++) {
    if(radios[i].checked === true) {
      return radios[i].value
    }
  }
  return ''
}

/**
 * Decodes comment before adding to DOM
 * @param {string} comment - comment content
 * @returns {string}
 */
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