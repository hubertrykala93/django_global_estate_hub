const $addPropertyForm = document.querySelector('[data-add-property-form]')

const itemsCounter = {
  'education': 1,
  'health': 1,
  'transportation': 1,
  'shopping': 1,
  increment: function (category) {
    itemsCounter[category]++
  }
}

const multipleRowItems = (e) => {
  if (!e.target.dataset.hasOwnProperty('addItem')) { return false }
  const $rowsContainer = e.target.parentElement
  const category = $rowsContainer.dataset.multiple

  const setRowContent = (category) => {
    const $row = document.createElement('div')
    $row.classList.add('form__row')

    $row.innerHTML = `
    <div class="form__field">
      <label for="${category}-name-${itemsCounter[category]}" class="form__label">name</label>
      <div class="form__input-wrap">
        <input data-${category}-name${itemsCounter[category] + 1} data-input type="text" id="${category}-name-${itemsCounter[category]}" name="${category}-name">
      </div>
    </div>

    <div class="form__field">
        <label for="${category}-distance-${itemsCounter[category]}" class="form__label">distance</label>
        <div class="form__input-wrap">
          <input data-${category}-distance${itemsCounter[category] + 1} data-input type="text" id="${category}-distance-${itemsCounter[category]}" name="${category}-distance">
        </div>
    </div>
    `
    itemsCounter.increment(category)
    return $row
  }
  
  const addRow = (container) => {
    container.append(setRowContent(category))
  }
  
  addRow($rowsContainer)
  
}

const ajaxSuccess = () =>{
  const xhr = new XMLHttpRequest()
  xhr.open('POST', 'create-property-success', true)
  xhr.setRequestHeader('X-CSRFToken', csrfToken)
  xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
  xhr.send({
    "success": true
  })

  // xhr.onreadystatechange = function () {
  //   if (this.readyState == 4 && this.status == 200) {
  //       const response = JSON.parse(this.responseText)
  //   }
  // }
}

const serverResponse = (response) => {
  console.log(response);

  const getFieldName = (key) => {
    switch (key) {
      case 'title':
        return 'data-title'
      case 'price':
        return 'data-price'
      case 'description':
        return 'data-description'
      case 'status':
        return 'data-status'
      case 'category':
        return 'data-category'
      case 'thumbnail':
        return 'data-thumbnail'
      case 'gallery':
        return 'data-gallery'
      case 'video':
        return 'data-video'
      case 'year_of_built':
        return 'data-year'
      case 'number_of_bedrooms':
        return 'data-bedrooms'
      case 'number_of_bathrooms':
        return 'data-bathrooms'
      case 'square_meters':
        return 'data-square-meters'
      case 'parking_space':
        return 'data-parking-space'
      case 'country':
        return 'data-countries-list'
      case 'province':
        return 'data-provinces-list'
      case 'city':
        return 'data-cities-list'
      case 'postal_code':
        return 'data-postal-code'
      case 'amenities':
        return 'data-amenity'
      case 'education_name':
        return 'data-education-name'
      case 'education_distance':
        return 'data-education-distance'
      case 'health_name':
        return 'data-health-name'
      case 'health_distance':
        return 'data-health-distance'
      case 'transportation_name':
        return 'data-transportation-name'
      case 'transportation_distance':
        return 'data-transportation-distance'
      case 'shopping_name':
        return 'data-shopping-name'
      case 'shopping_distance':
        return 'data-shopping-distance'
    }
  }

  const loopThroughResponse = (response) => {
    let allValid = true
    for (const [key, value] of Object.entries(response)) {
      if (Array.isArray(value)) {
        console.log(value)
        value.forEach((itemObj, index) => {
          for (const [key, value] of Object.entries(itemObj)) {
            const fieldName = getFieldName(key)
            if (!value.valid) { 
              showInfo(value.valid, value.message, $addPropertyForm, fieldName + (index + 1))
              allValid = false 
            } else {
              removeInfo($addPropertyForm, fieldName + (index + 1))
            }
          }
        })
      } else {
        const fieldName = getFieldName(key)
        if (!value.valid) { 
          showInfo(value.valid, value.message, $addPropertyForm, fieldName)
          allValid = false 
        } else {
          removeInfo($addPropertyForm, fieldName)
        }
      }
    }

    if (allValid) { 
      ajaxSuccess()
     }
  }

  loopThroughResponse(response)
}

const submitForm = (e) => {
  e.preventDefault()
  const urlValue = $addPropertyForm.querySelector('[name="url"]').value
  if ( !urlValue == '' ) { return false }

  const $formElements = $addPropertyForm.elements
  const data = new FormData($addPropertyForm)

  const ajaxRequest = (data) =>{
    const xhr = new XMLHttpRequest()
    xhr.open('POST', 'create-property', true)
    xhr.setRequestHeader('X-CSRFToken', csrfToken)
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    xhr.send(data)

    xhr.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
          const response = JSON.parse(this.responseText)
          serverResponse(response)
      }
    }
  }

  // const createNearbyItemsArray = (nameArr, distanceArr) => {
  //   const arr = []
  //   for (let i = 0; i < nameArr.length; i++) {
  //     const obj = {
  //       "name": nameArr[i],
  //       "distance": distanceArr[i]
  //     }
  //     arr.push(obj)
  //   }
  //   return arr
  // }

  // const data = {
  //   "title": [formData.get('title').trim(), "data-title", $formElements['title'].parentElement.parentElement.querySelector('.form__label').textContent],
  //   "price": [formData.get('price').trim(), "data-price", $formElements['price'].parentElement.parentElement.querySelector('.form__label').textContent],
  //   "description": [formData.get('description').trim(), "data-description", $formElements['description'].parentElement.parentElement.querySelector('.form__label').textContent],
  //   "listing_status": [formData.get('status'), "data-status", $formElements['status'][0].parentElement.parentElement.parentElement.querySelector('.form__label').textContent],
  //   "category": [formData.getAll('category'), "data-category", $formElements['category'][0].parentElement.parentElement.parentElement.querySelector('.form__label').textContent],
  //   "thumbnail": [$formElements['thumbnail'].files, "data-thumbnail", $formElements['thumbnail'].parentElement.parentElement.querySelector('.form__label').textContent],
  //   "gallery": [$formElements['gallery'].files, "data-gallery", $formElements['gallery'].parentElement.parentElement.querySelector('.form__label').textContent],
  //   "video": [$formElements['video'].files, "data-video", $formElements['video'].parentElement.parentElement.querySelector('.form__label').textContent],
  //   "year_of_built": [formData.get('year_of_built').trim(), "data-year", $formElements['year_of_built'].parentElement.parentElement.querySelector('.form__label').textContent],
  //   "number_of_bedrooms": [formData.get('number_of_bedrooms').trim(), "data-bedrooms", $formElements['number_of_bedrooms'].parentElement.parentElement.querySelector('.form__label').textContent],
  //   "number_of_bathrooms": [formData.get('number_of_bathrooms').trim(), "data-bathrooms", $formElements['number_of_bathrooms'].parentElement.parentElement.querySelector('.form__label').textContent],
  //   "square_meters": [formData.get('square_meters').trim(), "data-square-meters", $formElements['square_meters'].parentElement.parentElement.querySelector('.form__label').textContent],
  //   "parking_space": [formData.get('parking_space').trim(), "data-parking-space", $formElements['parking_space'].parentElement.parentElement.querySelector('.form__label').textContent],
  //   "postal_code": [formData.get('postal_code').trim(), "data-postal-code", $formElements['postal_code'].parentElement.parentElement.querySelector('.form__label').textContent],
  //   "city": [formData.get('city'), "data-city", 'city'],
  //   "province": [formData.get('province'), "data-province", 'province'],
  //   "country": [formData.get('country'), "data-country", 'country'],
  //   "amenities": [formData.getAll('amenities'), "data-amenity", $formElements['amenities'][0].parentElement.parentElement.parentElement.querySelector('.form__label').textContent],
  //   "education": [createNearbyItemsArray(formData.getAll('education-name'), formData.getAll('education-distance')), "data-education-name", "education"],
  //   "health_and_medical": [createNearbyItemsArray(formData.getAll('health-name'), formData.getAll('health-distance')), "data-health-name", "health"],
  //   "transportation": [createNearbyItemsArray(formData.getAll('transportation-name'), formData.getAll('transportation-distance')), "data-transportation-name", "transportation"],
  //   "shopping": [createNearbyItemsArray(formData.getAll('shopping-name'), formData.getAll('shopping-distance')), "data-shopping-name", "shopping"],
  // }



  console.log("wysłane ", data)


  ajaxRequest(data)
}

const getSelectedOptionValue = (inputs) => {
  if (!inputs.length) { return false }

  for (let i = 0; i < inputs.length; i++) {
    if (inputs[i].checked) { return inputs[i].value}
  }
  return false
} 

//Location settings
let chosenProvince = ''

const clearSelectChoice = (changedTarget) => {
  const $provincePlaceholder = $addPropertyForm.querySelector('[data-province-placeholder]')
  const $cityPlaceholder = $addPropertyForm.querySelector('[data-city-placeholder]')
  if (changedTarget === 'country') {
    $provincePlaceholder.textContent = 'Choose Province'
    $cityPlaceholder.textContent = 'Choose City'
    $addPropertyForm.querySelector('[data-provinces-list]').innerHTML = ''
  } else if (changedTarget === 'province') {
    $cityPlaceholder.textContent = 'Choose City'
  }
  $addPropertyForm.querySelector('[data-cities-list]').innerHTML = ''
}

const updateLocationOptions = (dropdownEl, itemsArr, name) => {
  const $dropdownParent = $addPropertyForm.querySelector(`[${dropdownEl}]`)
  $dropdownParent.innerHTML = ''

  let list = ''
  itemsArr.forEach(item => {
    if (item.name === chosenProvince) {
      list+= `
        <li role="option">
          <input data-option type="radio" value="${item.name}" id="${item.slug}" name="${name}" checked>
          <label for="${item.slug}">${item.name}</label>
        </li>
      `
    } else {
    list+= `
        <li role="option">
          <input data-option type="radio" value="${item.name}" id="${item.slug}" name="${name}">
          <label for="${item.slug}">${item.name}</label>
        </li>
      `
    }
  })
  $dropdownParent.insertAdjacentHTML('beforeend', list)
}

const selectAjaxRequest = (data) =>{
  const xhr = new XMLHttpRequest()
  xhr.open('POST', 'set-location', true)
  xhr.setRequestHeader('X-CSRFToken', csrfToken)
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
  xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
  xhr.send(JSON.stringify(data))

  xhr.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
        const response = JSON.parse(this.responseText)
        console.log("odebrane: ", response);
        updateLocationOptions('data-provinces-list', response.provinces, 'province')
        updateLocationOptions('data-cities-list', response.cities, 'city')
    }
  }
}

const selectHandler = (e) => {
  if (e.target.name === 'country' || e.target.name === 'province') {
    clearSelectChoice(e.target.name)
    
    const $countryInputs = $addPropertyForm.querySelectorAll('[name="country"]')
    const $provinceInputs = $addPropertyForm.querySelectorAll('[name="province"]')
    
    const data = {
      "country": getSelectedOptionValue($countryInputs),
      "province" : getSelectedOptionValue($provinceInputs)
    }
    
    chosenProvince = data.province
    
    console.log("wysłane: ", data);
    selectAjaxRequest(data)
  }
}

//Event listeners
$addPropertyForm.addEventListener('click', multipleRowItems)
$addPropertyForm.addEventListener('submit', submitForm)
$addPropertyForm.addEventListener('change', selectHandler)