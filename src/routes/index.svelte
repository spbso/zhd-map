<script lang="ts">
    import Panzoom from '@panzoom/panzoom'
    import InlineSVG from 'svelte-inline-svg';
    import map from '../data/Frame 1.svg';
    import {onMount} from "svelte";
    import locations from '../data/locations.json'
    import Tooltip from "../lib/Tooltip.svelte";


    let panzoom;
    let scale;
    let tooltipElements: string[] = [];

    onMount(() => {
        setTimeout(() => {
            const width = 904;
            const height = 844;

            let startScale = 1;

            // if (width < height) {
            //     startScale = window.innerWidth / width
            // } else {
            //     startScale = window.innerHeight / height
            // }

            const elem = document.getElementById('target-image')
            panzoom = Panzoom(elem, {
                minScale: startScale,
                maxScale: 5,
                contain: 'outside',
                cursor: 'arrow',
                roundPixels: true,
                // startX: 0,
                // startY: 0,
                // startX: -1 * Math.round(width / 2),
                // startY: -1 * Math.round(height / 2),
                startScale,
            });
            // panzoom.pan(0, 0)
            window['pz'] = panzoom
            window['map'] = elem

            elem.parentElement.addEventListener('wheel', panzoom.zoomWithWheel)
            elem.addEventListener('panzoomchange', (event) => {
                scale = event.detail.scale;
                // const tooltip = document.getElementById('tooltip')
                // tooltip.style.display = 'none'
                // console.log(event.detail) // => { x: 0, y: 0, scale: 1 }
            })

            Object.keys(locations).forEach(k => {
                const campfireId = locations[k]
                setTimeout(() => {
                    const campfireObject = document.getElementById(campfireId);
                    campfireObject.addEventListener('click', (e: MouseEvent) => {
                        console.log('campfire click', campfireObject)
                        document.querySelectorAll('.tooltip').forEach(tt => tt.classList.add('hidden'))
                        const tooltip = document.getElementById(`tooltip-${campfireId}`)
                        tooltip.classList.remove('hidden')
                        tooltip.click()
                    })
                }, 100)
            });
        }, 100)
    })

    let searchTerm = '';
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
        const campfire = document.getElementById(campfireId) as HTMLElement;

        // TODO Refactor
        console.log()
        document.querySelectorAll('.tooltip').forEach(tt => tt.classList.add('hidden'))
        const tooltip = document.getElementById(`tooltip-${campfireId}`)
        tooltip.classList.remove('hidden')
        tooltip.click()

        // TODO fix
        window['pz'].zoom(1)
        const cx = Number(campfire.attributes['cx'].value);
        const cy = Number(campfire.attributes['cy'].value);
        window['pz'].pan(window.innerWidth / 2 - cx, window.innerHeight / 2 - cy)

    }

    const mapClick = (e: MouseEvent) => {
        console.log(`client=(${e.clientX}, ${e.clientY}), offset=(${e.offsetX}, ${e.offsetY}), page=(${e.pageX}, ${e.pageY})`)
    }
</script>

<div class="w-screen h-screen m-0 overflow-hidden">
    <div class="tooltips">
        {#each Object.keys(locations) as campfire}
            <Tooltip {campfire}/>
        {/each}
    </div>
    <div class="absolute top-[3%] left-[5%] right-[5%] z-10">
        <div class="w-full">
            <input type="text"
                   class="block opacity-70 bg-[#3C241D] focus:opacity-100 text-white rounded-2xl px-5 py-2 w-full text-[24px]"
                   placeholder="Отряд или костёр..." bind:value={searchTerm} autocomplete="off"/>
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
        <InlineSVG src={map} id="target-image" on:click={mapClick}/>
    </div>
</div>
