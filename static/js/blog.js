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