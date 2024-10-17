function deleteVideo(videoId) {
    fetch("/deleteVido", {
      method: "POST",
      body: JSON.stringify({ videoId: videoId }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }