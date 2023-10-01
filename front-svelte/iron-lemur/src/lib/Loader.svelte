<script>
    export let isLoading = false;
</script>

{#if isLoading}
    <div class="loader">
        <div class="bar" />
    </div>
{/if}

<style>
    .loader {
        width: 100%;
        height: 8px;
        background-color: #f0f0f0;
        position: fixed; 
        bottom: 0;
        left: 0;
    }

    .bar {
        width: 0;
        height: 100%;
        background-color: #D28B00ee; /* Kolor paska postępu */
        animation: loading 4.5s linear infinite;
    }

    @keyframes loading {
        0% {
            width: 0;
        }
        50% {
            width: 50%;
        }
        100% {
            width: 100%;
        }
    }
</style>
