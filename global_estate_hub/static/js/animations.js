/**
   * PAGE TITLE
    */

const $pageTitle = document.querySelector('.page-title')

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

ScrollReveal().reveal('.page-title .title', titleAnimation)
ScrollReveal().reveal('.page-title .breadcrumbs li', breadcrumbsListItems)
}