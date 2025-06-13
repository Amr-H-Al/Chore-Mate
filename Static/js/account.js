  // Function to adjust the width of an input based on its content
  function adjustInputWidth(input) {
    const temporarySpan = document.createElement("span");
    temporarySpan.style.visibility = "hidden";
    temporarySpan.style.whiteSpace = "nowrap";
    temporarySpan.style.font = window.getComputedStyle(input).font;
    temporarySpan.innerText = input.value || input.placeholder;
    document.body.appendChild(temporarySpan);

    const newWidth = Math.max(temporarySpan.offsetWidth + 10, 50); // Minimum width is 50px
    input.style.width = `${newWidth}px`;

    document.body.removeChild(temporarySpan);
}

// Apply the resizing function to all inputs on the page
document.querySelectorAll('input[type="text"]').forEach(input => {
    adjustInputWidth(input);

    // Update width dynamically when the content changes
    input.addEventListener('input', () => adjustInputWidth(input));
});