const cards = document.querySelectorAll(".shoe-card");
const dialog = document.querySelector("#shoe-dialog");
const dialogImage = document.querySelector("#dialog-image");
const dialogBrand = document.querySelector("#dialog-brand");
const dialogTitle = document.querySelector("#dialog-title");
const dialogColorway = document.querySelector("#dialog-colorway");
const dialogMaterial = document.querySelector("#dialog-material");
const ratingStatus = document.querySelector("#rating-status");
const ratingStars = document.querySelectorAll(".rating-star");
const closeButton = document.querySelector(".dialog-close");

function readRating(shoeId) {
  try {
    const savedRating = Number(localStorage.getItem(`shoe-rating-${shoeId}`));
    return Number.isInteger(savedRating) && savedRating >= 1 && savedRating <= 5
      ? savedRating
      : 0;
  } catch (error) {
    console.error("Unable to read the saved shoe rating.", error);
    return 0;
  }
}

function updateCardRating(card, rating) {
  const summary = card.querySelector(".rating-summary");
  summary.textContent = rating ? `${"★".repeat(rating)}${"☆".repeat(5 - rating)} · ${rating}/5` : "Click to rate this pair";
}

function updateStarSelection(rating) {
  ratingStars.forEach((star) => {
    const isSelected = Number(star.dataset.rating) <= rating;
    star.classList.toggle("is-selected", isSelected);
    star.setAttribute("aria-pressed", String(Number(star.dataset.rating) === rating));
  });
}

let selectedCard;

cards.forEach((card) => {
  updateCardRating(card, readRating(card.dataset.shoeId));

  card.addEventListener("click", () => {
    selectedCard = card;
    dialogImage.src = card.dataset.image;
    dialogImage.alt = `${card.dataset.brand} ${card.dataset.style}`;
    dialogBrand.textContent = card.dataset.brand;
    dialogTitle.textContent = card.dataset.style;
    dialogColorway.textContent = card.dataset.colorway;
    dialogMaterial.textContent = card.dataset.material;
    dialogMaterial.hidden = !card.dataset.material;
    const rating = readRating(card.dataset.shoeId);
    updateStarSelection(rating);
    ratingStatus.textContent = rating ? `Your current rating: ${rating} out of 5.` : "Choose a star to rate this pair.";
    dialog.showModal();
  });
});

ratingStars.forEach((star) => {
  star.addEventListener("click", () => {
    if (!selectedCard) {
      return;
    }

    const rating = Number(star.dataset.rating);
    try {
      localStorage.setItem(`shoe-rating-${selectedCard.dataset.shoeId}`, String(rating));
      updateStarSelection(rating);
      updateCardRating(selectedCard, rating);
      ratingStatus.textContent = `Your rating of ${rating} out of 5 was saved in this browser.`;
    } catch (error) {
      console.error("Unable to save the shoe rating.", error);
      ratingStatus.textContent = "Could not save your rating. Check browser storage permissions.";
    }
  });
});

closeButton.addEventListener("click", () => dialog.close());

dialog.addEventListener("click", (event) => {
  if (event.target === dialog) {
    dialog.close();
  }
});