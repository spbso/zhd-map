<script lang="ts">
    import Panzoom from '@panzoom/panzoom'
    import {onMount} from "svelte";
    import locations from '../data/locations.json'
    import Tooltip from "../lib/Tooltip.svelte";
    import {getCampfire} from "../lib/helpers";
    import frame from '../data/Frame 1.svg'
    import InlineSvg from "svelte-inline-svg";


    let panzoom;
    let scale;

    function initMap() {
        console.log('init map')
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
            minScale: startScale,
            maxScale: 5,
            contain: 'outside',
            cursor: 'arrow',
            roundPixels: true,
            // startX: -1 * Math.round(width / 2),
            // startY: -1 * Math.round(height / 2),
            startScale,
        });
        // panzoom.pan(0, 0)
        window['pz'] = panzoom
        window['map'] = elem

        elem.parentElement.addEventListener('wheel', panzoom.zoomWithWheel)

        Object.keys(locations).forEach(k => {
            const campfireId = locations[k]
            setTimeout(() => {
                const campfireObject = getCampfire(campfireId);
                campfireObject.addEventListener('click', (e: MouseEvent) => {
                    document.querySelectorAll('.tooltip').forEach(tt => tt.classList.add('hidden'))
                    const tooltip = document.getElementById(`tooltip-${campfireId}`)
                    tooltip.classList.remove('hidden')
                    tooltip.click()
                })
            }, 100)
        });
    }


    onMount(() => {
        setTimeout(() => {
            initMap();
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
        const campfire = getCampfire(campfireId);

        // TODO Refactor
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
        <InlineSvg src={frame} id="target-image"/>
    </div>
</div>
