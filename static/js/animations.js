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
   * REUSABLE ANIMATIONS
    */

const $fadeFromLeft = document.querySelectorAll('[data-animation-fade-from-left]')
const fadeFromLeft = {
  distance: '40px',
  origin: 'left',
  opacity: 0,
  duration: 800,
  easing: 'ease-in-out',
  interval: 90
}

const $fadeFromRight = document.querySelectorAll('[data-animation-fade-from-right]')
const fadeFromRight = {
  distance: '40px',
  origin: 'right',
  opacity: 0,
  duration: 800,
  easing: 'ease-in-out',
  interval: 90
}

const $fadeFromBottom = document.querySelectorAll('[data-animation-fade-from-bottom]')
const fadeFromBottom = {
  distance: '20px',
  origin: 'bottom',
  opacity: 0,
  duration: 800,
  easing: 'ease-in-out',
  interval: 90
}

ScrollReveal().reveal($fadeFromRight, fadeFromRight)
ScrollReveal().reveal($fadeFromLeft, fadeFromLeft)
ScrollReveal().reveal($fadeFromBottom, fadeFromBottom)