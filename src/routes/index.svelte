<script lang="ts">
    import Panzoom from '@panzoom/panzoom'
    import InlineSVG from 'svelte-inline-svg';
    import map from '../data/Frame.svg';
    import {onMount} from "svelte";
    import locations from '../data/locations.json'


    let panzoom;

    onMount(() => {
        const width = 904;
        const height = 844;
        let startScale = 1;
        if (width < height) {
            startScale = window.innerWidth / width
        } else {
            startScale = window.innerHeight / height
        }
        const elem = document.getElementById('target-image')
        panzoom = Panzoom(elem, {
            maxScale: 5,
            contain: 'outside',
            startX: -1 * Math.round(width / 2),
            startY: -1 * Math.round(height / 2),
            startScale
        });
        elem.parentElement.addEventListener('wheel', panzoom.zoomWithWheel)
        elem.addEventListener('panzoomchange', (event) => {
            // console.log(event.detail) // => { x: 0, y: 0, scale: 1 }
        })
    })

    let searchTerm: string;
    let candidates: string[] = [];

    $: {
        if (searchTerm) {
            const normalizedTerm = searchTerm.trim().toLowerCase();
            candidates = Object.keys(locations).filter((k: string) => k.toLowerCase().includes(normalizedTerm))
        }
    }

    const showCampfire = (identifier: string) => {
        searchTerm = '';
        const campfireId = locations[identifier];
        const mapSvg = document.getElementById('target-image')
        const campfire = document.querySelector(`.${campfireId}`);
        panzoom.zoom(2);
        panzoom.pan(0, 0);
    }
</script>

<div class="w-screen h-screen m-0 overflow-hidden">
    <div class="absolute top-[3%] left-[5%] right-[5%] z-10">
        <div class="w-full">
            <input type="text"
                   class="block opacity-70 bg-[#3C241D] focus:opacity-100 text-white rounded-2xl px-5 py-2 w-full text-[24px]"
                   placeholder="Отряд или костёр..." bind:value={searchTerm}/>
        </div>
        {#if searchTerm && searchTerm.length >= 2}
            {#if candidates && candidates.length > 0}
                <div class="bg-[#3C241D] rounded-2xl px-5 py-2 w-full text-[24px] mt-5 text-white">
                    {#each candidates as candidate}
                        <div class="hover:brightness-50 cursor-pointer leading-relaxed"
                             on:click={() => showCampfire(candidate)}>
                            {candidate}
                        </div>
                    {/each}
                </div>
            {:else}
                <div class="bg-[#3C241D] rounded-2xl px-5 py-2 w-full text-[24px] mt-5 text-[#FF6F6F]">
                    На карте такого нет. Точно не ошибся в названии?
                </div>
            {/if}
        {/if}
    </div>
    <div class="max-w-full max-h-full">
        <InlineSVG src={map} id="target-image"/>
    </div>
</div>
