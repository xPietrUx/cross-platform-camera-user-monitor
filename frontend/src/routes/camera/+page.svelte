<script lang="ts">
    const videoStreamUrl = 'http://127.0.0.1:8000/video/stream';
</script>


    <div class="video-wrapper">
        <img src={videoStreamUrl} alt="Strumień wideo z kamery" />
    </div>

    <style>
        .video-wrapper {
            height: 100%;
            width: 100%;
        }
    </style>
