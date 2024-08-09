window.addEventListener("load", (e) => {
  /**
   * @type {HTMLDivElement}
   */
  var image_viewport = document.querySelector("#image_viewport");

  /**
   * @type {HTMLDivElement}
   */
  var image_wrapper = document.querySelector("#image_wrapper");

  /**
   * @type {HTMLDivElement}
   */
  const create_comment = document.querySelector("#create_comment");

  /**
   * @type {HTMLDivElement}
   */
  var comments_div = document.querySelector("#comments");

  function updateComments() {
    var comments = document.querySelectorAll(".comment");

    comments.forEach((comment) => {
      comment.addEventListener("click", syncCommentToBox);

      var replyButton = comment.querySelector("#reply");
      replyButton.addEventListener("click", createReply);
    });
  }

  function updateBoxes() {
    var boxes = document.querySelectorAll(".box");

    boxes.forEach((box) => {
      box.addEventListener("click", syncBoxToComment);
    });
  }

  /**
   * @param {HTMLDivElement} image_viewport
   * @param {HTMLDivElement} image_wrapper
   */
  function centerImage(image_viewport, image_wrapper) {
    const image_viewport_style = window.getComputedStyle(image_viewport);
    const image_viewport_width = parseFloat(image_viewport_style.width);
    const image_viewport_height = parseFloat(image_viewport_style.height);

    const image_wrapper_style = window.getComputedStyle(image_wrapper);
    const image_wrapper_width = parseFloat(image_wrapper_style.width);
    const image_wrapper_height = parseFloat(image_wrapper_style.height);

    const image_ratio = image_wrapper_width / image_wrapper_height;

    const safeHeight = image_viewport_height * 0.8;
    const newWidth = safeHeight * image_ratio;

    const yPadding = (safeHeight * 0.2) / 2;
    const xPadding = (image_viewport_width - newWidth) / 2;

    image_wrapper.style.top = `${yPadding}px`;
    image_wrapper.style.left = `${xPadding}px`;
    image_wrapper.style.width = `${newWidth}px`;
    image_wrapper.style.height = `${safeHeight}px`;
  }

  /**
   * @param {WheelEvent} event
   * @param {number} magnitude
   * @param {HTMLDivElement} image_wrapper
   */
  function scaleImage(event, magnitude, image_wrapper) {
    const image_wrapper_style = window.getComputedStyle(image_wrapper);
    const image_wrapper_top = parseFloat(image_wrapper_style.top);
    const image_wrapper_left = parseFloat(image_wrapper_style.left);

    const image_wrapper_width = parseFloat(image_wrapper_style.width);
    const image_wrapper_height = parseFloat(image_wrapper_style.height);

    if (image_wrapper_width < 100 && magnitude < 1) {
      return;
    }

    if (image_wrapper_height < 100 && magnitude < 1) {
      return;
    }

    const rect = image_wrapper.getBoundingClientRect();
    const relativeX = event.clientX - rect.left;
    const relativeY = event.clientY - rect.top;

    const new_width = image_wrapper_width * magnitude;
    const new_height = image_wrapper_height * magnitude;

    // Calculate the new top and left based on the cursor position
    const new_left = image_wrapper_left - relativeX * (magnitude - 1);
    const new_top = image_wrapper_top - relativeY * (magnitude - 1);

    image_wrapper.style.width = `${new_width}px`;
    image_wrapper.style.height = `${new_height}px`;

    image_wrapper.style.top = `${new_top}px`;
    image_wrapper.style.left = `${new_left}px`;
  }

  function scrollImageViewport(event) {
    const image_wrapper = document.getElementById("image_wrapper");
    const magnitude = event.deltaY < 0 ? 1.2 : 0.8;
    scaleImage(event, magnitude, image_wrapper);
  }

  // Dragging logic
  let isDragging = false;
  let isShiftDragging = false;
  let isCreatingComment = false;

  let lastX = 0;
  let lastY = 0;
  let newCommentBox = null;

  function startDrag(event) {
    if (event.shiftKey && !isCreatingComment) {
      isShiftDragging = true;
      const rect = image_wrapper.getBoundingClientRect();
      const relativeX = ((event.clientX - rect.left) / rect.width) * 100;
      const relativeY = ((event.clientY - rect.top) / rect.height) * 100;

      newCommentBox = document.createElement("div");
      newCommentBox.style.position = "absolute";
      newCommentBox.style.top = `${relativeY}%`;
      newCommentBox.style.left = `${relativeX}%`;
      newCommentBox.style.width = "0%";
      newCommentBox.style.height = "0%";
      newCommentBox.classList.add(
        "absolute",
        "border-red-400",
        "border-2",
        "border-solid",
        "rounded-sm",
        "focus:border-red-900",
        "focus:bg-red-900",
        "focus:opacity-50",
        "box",
      );

      image_wrapper.appendChild(newCommentBox);
    } else {
      isDragging = true;
    }

    lastX = event.clientX;
    lastY = event.clientY;
    event.preventDefault();
  }

  function dragImage(event) {
    if (isDragging) {
      const dx = event.clientX - lastX;
      const dy = event.clientY - lastY;

      const style = window.getComputedStyle(image_wrapper);
      const top = parseFloat(style.top);
      const left = parseFloat(style.left);

      image_wrapper.style.top = `${top + dy}px`;
      image_wrapper.style.left = `${left + dx}px`;

      lastX = event.clientX;
      lastY = event.clientY;
    } else if (isShiftDragging) {
      const rect = image_wrapper.getBoundingClientRect();
      const relativeX = ((event.clientX - rect.left) / rect.width) * 100;
      const relativeY = ((event.clientY - rect.top) / rect.height) * 100;

      const startX = parseFloat(newCommentBox.style.left);
      const startY = parseFloat(newCommentBox.style.top);

      const width = relativeX - startX;
      const height = relativeY - startY;

      newCommentBox.style.width = `${width}%`;
      newCommentBox.style.height = `${height}%`;
    }
  }

  function stopDrag() {
    isDragging = false;
    if (isShiftDragging) {
      isCreatingComment = true;
      createComment();
    }
    isShiftDragging = false;
  }

  function scrollImageViewport(event) {
    const image_wrapper = document.getElementById("image_wrapper");
    const magnitude = event.deltaY < 0 ? 1.2 : 0.8;
    scaleImage(event, magnitude, image_wrapper);
  }

  function createComment() {
    var new_create_comment = create_comment.cloneNode(true);
    new_create_comment = comments_div.appendChild(new_create_comment);
    new_create_comment.style.display = "inherit";

    var cancelButton = new_create_comment.querySelector("#cancel");
    var submitButton = new_create_comment.querySelector("#submit");

    cancelButton.addEventListener("click", discardComment);
    submitButton.addEventListener("click", submitComment);
  }

  function createReply(event) {
    var new_create_reply = create_comment.cloneNode(true);
    new_create_reply = this.parentNode.parentNode.appendChild(new_create_reply);
    new_create_reply.style.display = "inherit";

    var cancelButton = new_create_reply.querySelector("#cancel");
    var submitButton = new_create_reply.querySelector("#submit");

    cancelButton.addEventListener("click", discardReply);
    submitButton.addEventListener("click", submitReply);
    event.stopPropagation();
  }

  async function submitComment() {
    const { top, left, width, height } = newCommentBox.style;

    try {
      const response = await fetch("/comment", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          top,
          left,
          width,
          height,
          content: document.querySelector("#new_comment_textarea").value,
          id: window.location.pathname.split("/").filter(Boolean).pop(),
        }),
      });

      if (!response.ok) throw new Error("Network response was not ok.");

      var newCommentDiv = document.createElement("div");
      newCommentDiv = comments_div.insertBefore(
        newCommentDiv,
        comments_div.lastChild,
      );
      newCommentDiv.outerHTML = await response.text();

      comments_div.lastChild.remove();

      var instantiatedCommentDiv = comments_div.lastChild;

      if (comments_div.lastChild) {
        instantiatedCommentDiv.tabIndex = comments_div.lastChild.tabIndex + 1;
      } else {
        instantiatedCommentDiv.tabIndex = 0;
      }

      newCommentBox.id = instantiatedCommentDiv.id;
      newCommentBox.tabIndex = -1;
      instantiatedCommentDiv.focus();

      updateComments();
      updateBoxes();
    } catch (error) {
      console.error("Error:", error);
    }

    isCreatingComment = false;
  }

  async function submitReply() {
    var commentNode = document.querySelector("#new_comment_textarea").parentNode
      .parentNode;

    try {
      const response = await fetch("/reply", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          content: document.querySelector("#new_comment_textarea").value,
          file_id: window.location.pathname.split("/").filter(Boolean).pop(),
          comment_id: commentNode.id,
        }),
      });

      if (!response.ok) throw new Error("Network response was not ok.");

      var newReplyDiv = document.createElement("div");
      newReplyDiv = commentNode.appendChild(newReplyDiv);
      newReplyDiv.outerHTML = await response.text();

      document.querySelector("#new_comment_textarea").parentNode.remove();
    } catch (error) {
      console.error("Error:", error);
    }
  }

  function discardComment() {
    isCreatingComment = false;
    comments_div.children.item(comments_div.children.length - 1).remove();
    newCommentBox.remove();
  }

  function discardReply() {
    this.parentNode.parentNode.remove();
  }

  function syncCommentToBox(event) {
    if (event.target == document.querySelector("#new_comment_textarea")) {
      return;
    }
    var box = document.querySelector(`#image_wrapper #${this.id}`);
    box.focus();
  }

  function syncBoxToComment(event) {
    var comment = document.querySelector(`#comments #${this.id}`);
    comment.focus();
  }

  centerImage(image_viewport, image_wrapper);
  updateComments();
  updateBoxes();

  image_viewport.addEventListener("wheel", scrollImageViewport);
  image_viewport.addEventListener("mousedown", startDrag);
  document.addEventListener("mousemove", dragImage);
  document.addEventListener("mouseup", stopDrag);
});
