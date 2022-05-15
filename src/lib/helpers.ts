const campfireById = (id: string): HTMLElement => {
    return document.getElementById(id) as HTMLElement
}

const campfireByClass = (id: string): HTMLElement => {
    return document.querySelector(`.${id}`) as HTMLElement
}

export const getCampfire = campfireById
