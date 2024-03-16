document.addEventListener("DOMContentLoaded", function () {
  const uploadButton = document.getElementById("upload-button");
  const fileInput = document.getElementById("file-upload");

  uploadButton.addEventListener("click", function () {
    fileInput.click(); // Trigger the file input click event
  });

  fileInput.addEventListener("change", function () {
    const file = this.files[0]; // Get the selected file

    // Create FormData object to send file data
    const formData = new FormData();
    formData.append("image", file);

    // Display the selected image immediately
    const uploadedImageContainer = document.createElement("div");
    uploadedImageContainer.className = "uploaded-image-container";
    const img = document.createElement("img");
    img.src = URL.createObjectURL(file);
    uploadedImageContainer.appendChild(img);

    // Send POST request to server to handle the file upload
    fetch("/upload", {
      method: "POST",
      body: formData,
      headers: {
        "X-CSRFToken": getCookie("csrftoken"), // Include CSRF token
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          // If there's an error returned by the server (e.g., image is not a dog)
          alert(data.error); // Display the error message in an alert
        } else {
          // Reload the page to display the newly uploaded image
          window.location.reload();
        }
      })
      .catch((error) => console.error("Error:", error));
  });

  // Function to get CSRF token from cookies
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});
