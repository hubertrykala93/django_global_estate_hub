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
  #OTHER
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