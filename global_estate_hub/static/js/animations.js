/**
   * PAGE TITLE
    */

const $pageTitle = document.querySelector('[data-pagetitle-animation]')

if ( $pageTitle ){

const titleAnimation = {
  delay: 100,
  distance: '100px',
  duration: 700,
  opacity: .01,
  origin: 'right',
  easing: 'linear'
}

const breadcrumbsListItems = {
  delay: 200,
  distance: '30px',
  duration: 1000,
  origin: 'bottom',
  interval: 150,
}

ScrollReveal().reveal($pageTitle.querySelector('.title'), titleAnimation)
ScrollReveal().reveal($pageTitle.querySelectorAll('.breadcrumbs li'), breadcrumbsListItems)
}


/**
   * HOME PAGE
    */

const $aboutSection = document.querySelector('[data-aboutsection-animation]')

if($aboutSection){

  const singleImageAnimation = {
    delay: 200,
    distance: '30px',
    duration: 900,
    opacity: 0,
    origin: 'left',
    easing: 'ease'
  }

  const doubleImageTopAnimation = {
    delay: 250,
    distance: '30px',
    duration: 900,
    opacity: 0,
    origin: 'top',
    easing: 'ease'
  }

  const doubleImageBottomAnimation = {
    delay: 300,
    distance: '30px',
    duration: 900,
    opacity: 0,
    origin: 'bottom',
    easing: 'ease'
  }

  const listAnimation = {
    delay: 100,
    distance: '50px',
    duration: 900,
    opacity: 0,
    origin: 'right',
    easing: 'ease',
    interval: 150,
  }

  ScrollReveal().reveal($aboutSection.querySelector('.image.single'), singleImageAnimation)
  ScrollReveal().reveal($aboutSection.querySelector('.image.top'), doubleImageTopAnimation)
  ScrollReveal().reveal($aboutSection.querySelector('.image.bottom'), doubleImageBottomAnimation)
  ScrollReveal().reveal($aboutSection.querySelectorAll('.about__list .about__list-item'), listAnimation)
}


/**
   * -SECTION TITLE
    */

const $sectionTitles = document.querySelectorAll('[data-sectiontitle-animation]')

if ($sectionTitles.length){
  const upperTitleAnimation = {
    delay: 250,
    distance: '30px',
    duration: 700,
    opacity: 0,
    origin: 'bottom',
    easing: 'ease'
  }

  const mainTitleAnimation = {
    delay: 350,
    distance: '30px',
    duration: 700,
    opacity: 0,
    origin: 'bottom',
    easing: 'ease'
  }

  $sectionTitles.forEach(item => {
    const upperTitle = item.querySelector('.upper-title')
    const mainTitle = item.querySelector('.main-title')

    if(upperTitle){
      ScrollReveal().reveal(upperTitle, upperTitleAnimation)
    }
    if(mainTitle){
      ScrollReveal().reveal(mainTitle, mainTitleAnimation)
    }
  });

}


/**
   * FAQ
    */

const $faqSection = document.querySelector('[data-faq-animation]')

if ($faqSection) {
  const accordionItemsAnimation = {
    delay: 100,
    distance: '50px',
    duration: 900,
    opacity: 0,
    origin: 'bottom',
    easing: 'ease',
    interval: 150,
  }

  const ImageAnimation = {
    delay: 300,
    distance: '200px',
    duration: 900,
    opacity: 0,
    origin: 'right',
    easing: 'ease-out'
  }

  ScrollReveal().reveal($faqSection.querySelectorAll('.theme-accordion .accordion__item'), accordionItemsAnimation)
  ScrollReveal().reveal($faqSection.querySelector('.faq__image'), ImageAnimation)
}