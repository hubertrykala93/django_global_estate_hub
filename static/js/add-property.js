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
        <input data-${category}-name data-input type="text" id="${category}-name-${itemsCounter[category]}" name="${category}-name">
      </div>
    </div>

    <div class="form__field">
        <label for="${category}-distance-${itemsCounter[category]}" class="form__label">distance</label>
        <div class="form__input-wrap">
          <input data-${category}-distance data-input type="text" id="${category}-distance-${itemsCounter[category]}" name="${category}-distance">
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

const submitForm = (e) => {
  e.preventDefault()
  const $formElements = $addPropertyForm.elements
  const formData = new FormData($addPropertyForm)

  const ajaxRequest = (data) =>{
    const xhr = new XMLHttpRequest()
    xhr.open('POST', 'create-property', true)
    xhr.setRequestHeader('X-CSRFToken', csrfToken)
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    xhr.send(JSON.stringify(data))

    xhr.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
          const response = JSON.parse(this.responseText)
          // serverResponse(response)
          console.log("odebrane: ", response);
      }
    }
  }

  const createNearbyItemsArray = (nameArr, distanceArr) => {
    const arr = []
    for (let i = 0; i < nameArr.length; i++) {
      const obj = {
        "name": nameArr[i],
        "distance": distanceArr[i]
      }
      arr.push(obj)
    }
    return arr
  }

  const data = {
    "title": [formData.get('title').trim(), "data-title", $formElements['title'].parentElement.parentElement.querySelector('.form__label').textContent],
    "price": [formData.get('price').trim(), "data-price", $formElements['price'].parentElement.parentElement.querySelector('.form__label').textContent],
    "description": [formData.get('description').trim(), "data-description", $formElements['description'].parentElement.parentElement.querySelector('.form__label').textContent],
    "listing_status": [formData.get('status'), "data-status", $formElements['status'][0].parentElement.parentElement.parentElement.querySelector('.form__label').textContent],
    "category": [formData.getAll('category'), "data-category", $formElements['category'][0].parentElement.parentElement.parentElement.querySelector('.form__label').textContent],
    "images": [$formElements['images'].files, "data-images", $formElements['images'].parentElement.parentElement.querySelector('.form__label').textContent],
    "video": [$formElements['video'].files, "data-video", $formElements['video'].parentElement.parentElement.querySelector('.form__label').textContent],
    "year_of_built": [formData.get('year_of_built').trim(), "data-year", $formElements['year_of_built'].parentElement.parentElement.querySelector('.form__label').textContent],
    "number_of_bedrooms": [formData.get('number_of_bedrooms').trim(), "data-bedrooms", $formElements['number_of_bedrooms'].parentElement.parentElement.querySelector('.form__label').textContent],
    "number_of_bathrooms": [formData.get('number_of_bathrooms').trim(), "data-bathrooms", $formElements['number_of_bathrooms'].parentElement.parentElement.querySelector('.form__label').textContent],
    "square_meters": [formData.get('square_meters').trim(), "data-square-meters", $formElements['square_meters'].parentElement.parentElement.querySelector('.form__label').textContent],
    "parking_space": [formData.get('parking_space').trim(), "data-parking-space", $formElements['parking_space'].parentElement.parentElement.querySelector('.form__label').textContent],
    "postal_code": [formData.get('postal_code').trim(), "data-postal-code", $formElements['postal_code'].parentElement.parentElement.querySelector('.form__label').textContent],
    "city": [formData.get('city').trim(), "data-city", $formElements['city'].parentElement.parentElement.querySelector('.form__label').textContent],
    "province": [formData.get('province').trim(), "data-province", $formElements['province'].parentElement.parentElement.querySelector('.form__label').textContent],
    "country": [formData.get('country').trim(), "data-country", $formElements['country'].parentElement.parentElement.querySelector('.form__label').textContent],
    "amenities": [formData.getAll('amenities'), "data-amenity", $formElements['amenities'][0].parentElement.parentElement.parentElement.querySelector('.form__label').textContent],
    "education": [createNearbyItemsArray(formData.getAll('education-name'), formData.getAll('education-distance')), "data-education-name", "education"],
    "health_and_medical": [createNearbyItemsArray(formData.getAll('health-name'), formData.getAll('health-distance')), "data-health-name", "health"],
    "transportation": [createNearbyItemsArray(formData.getAll('transportation-name'), formData.getAll('transportation-distance')), "data-transportation-name", "transportation"],
    "shopping": [createNearbyItemsArray(formData.getAll('shopping-name'), formData.getAll('shopping-distance')), "data-shopping-name", "shopping"],
  }

//  const data = new FormData()
//  data.append('images', $formElements['images'].files[0])

//  console.log("wysłane ", data.get('images'))
//  console.log($formElements['images'].files)

  ajaxRequest(data)
}

const getSelectedOptionValue = (inputs) => {
  if (!inputs.length) { return false }

  for (let i = 0; i < inputs.length; i++) {
    if (inputs[i].checked) { return inputs[i].value}
  }
  return false
} 

const updateLocationOptions = (dropdownEl, itemsArr, name) => {
  const $dropdownParent = $addPropertyForm.querySelector(`[${dropdownEl}]`)
  if (itemsArr.length === 0) { $dropdownParent.innerHTML = '' }

  let list = ''
  itemsArr.forEach(item => {
    list+= `
    <li role="option">
      <input data-option type="radio" value="${item.name}" id="${item.slug}" name="${name}">
      <label for="${item.slug}">${item.name}</label>
    </li>
    `
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
        // serverResponse(response)
        console.log("odebrane: ", response);
        updateLocationOptions('data-provinces-list', response.provinces, 'province')
        updateLocationOptions('data-cities-list', response.cities, 'city')
    }
  }
}

const selectHandler = (e) => {
  if (e.target.name === 'country' || e.target.name === 'province') {
    const $countryInputs = $addPropertyForm.querySelectorAll('[name="country"]')
    const $provinceInputs = $addPropertyForm.querySelectorAll('[name="province"]')

    const data = {
      "country": getSelectedOptionValue($countryInputs),
      "province" : getSelectedOptionValue($provinceInputs)
    }
    console.log("wysłane: ", data);
    selectAjaxRequest(data)
  }
}

$addPropertyForm.addEventListener('click', multipleRowItems)
$addPropertyForm.addEventListener('submit', submitForm)
$addPropertyForm.addEventListener('change', selectHandler)