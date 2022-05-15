<script lang="ts">
    import {onMount} from "svelte";
    import {computePosition, flip, shift, offset, arrow} from '@floating-ui/dom';

    export let campfire = "";
    import locations from '../data/locations.json'

    const tooltipElements = campfire.split(',')
    const campfireId = locations[campfire];

    export function placeTooltip(e: PointerEvent | null) {
        const arrowElement = document.getElementById(`arrow-${campfireId}`)
        const parent = document.getElementById(campfireId)
        const tooltip = document.getElementById(`tooltip-${campfireId}`)
        if (!parent) {
            throw Error("Didn't load " + campfireId)
        }
        computePosition(parent, tooltip, {
            placement: "top",
            middleware: [offset(6), flip(), shift(), arrow({element: arrowElement})],
        }).then(({x, y, placement, middlewareData}) => {
            Object.assign(tooltip.style, {
                left: `${x}px`,
                top: `${y}px`,
            });

            const {x: arrowX, y: arrowY} = middlewareData.arrow;

            const staticSide = {
                top: 'bottom',
                right: 'left',
                bottom: 'top',
                left: 'right',
            }[placement.split('-')[0]];

            Object.assign(arrowElement.style, {
                left: arrowX != null ? `${arrowX}px` : '',
                top: arrowY != null ? `${arrowY}px` : '',
                right: '',
                bottom: '',
                [staticSide]: '-4px',
            });
        });
        // if (e) {
        //     window['pz'].zoom(2);
        // }
    }

    onMount(() => {
        setTimeout(() => {
            placeTooltip(null);
            window['map'].addEventListener('panzoomchange', () => {
                placeTooltip(null);
            });
        }, 500)
    })
</script>

<div class="text-left text-white block absolute z-10 pointer-events-none hidden tooltip" id="tooltip-{campfireId}"
     on:click={placeTooltip}>
    {#each tooltipElements as element, index}
        <div class="bg-[#3C241D] px-1.5 bg-opacity-90">
            {element}
        </div>
    {/each}
    <div id="arrow-{campfireId}" class="absolute bg-[#3C241D] w-[8px] h-[8px] rotate-45"></div>
    <!--    <div class="w-0 h-0 border-l-[80px] border-l-transparent border-r-[80px] border-r-transparent border-opacity-90 border-t-[20px] border-t-[#3C241D]">-->
    <!--    </div>-->
</div>
