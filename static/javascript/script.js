const questions = document.querySelectorAll(".question");

questions.forEach(function (question) {
  const btn = question.querySelector(".faq-toggle");
  const answer = question.querySelector(".faq-answer");

  btn.addEventListener("click", function () {
    question.classList.toggle("show-text");

    // Smooth height transition
    if (question.classList.contains("show-text")) {
      answer.style.maxHeight = answer.scrollHeight + "px";
    } else {
      answer.style.maxHeight = null;
    }
  });
});

// // Biar pas ke login page gak reload
// document
//   .querySelector(".call-to-action")
//   .addEventListener("click", function (e) {
//     // Jangan mencegah default behavior untuk login link
//     console.log("Navigating to login page...");
//   });
