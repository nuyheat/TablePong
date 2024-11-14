import { Component } from "../../core/core.js";

export class Input extends Component {
	constructor(props = {}) {
		super({
			props : {
				className: 'row align-items-center', // 변경: form-group에서 row align-items-center로
			},
		});

		const {
			label = 'none',
			labelPosition = 'top',
			id = '',
			defaultValue = '',
			placeholder = '',
			type = 'text',
			variant = 'default',
			size = 'm',
		} = props;

		// label에 값이 있는 경우에만 label 엘리먼트 추가
		const labelEl = document.createElement('label');
		if (label !== 'none') {
			labelEl.textContent = label;
			labelEl.setAttribute('for', id);
			labelEl.classList.add('col-form-label', 'fw-bold'); // fw-bold 클래스 추가
			if (labelPosition === 'left') {
				labelEl.classList.add('col-sm-2');
			}
			if (labelPosition === 'top') {
				labelEl.classList.add('col-sm-10');
			}
			this.el.appendChild(labelEl);
		}

		const inputEl = document.createElement('input');
		inputEl.setAttribute('id', id);
		inputEl.value = defaultValue;
		inputEl.setAttribute('placeholder', placeholder);
		inputEl.setAttribute('type', type);
		inputEl.classList.add('form-control');

		switch (variant) {
			case 'background':
				inputEl.classList.add('input-background');
				break;
			default:
				// 기본은 bright
				inputEl.classList.add('input-bright');
		}``

		switch (size) {
			case 's':
				inputEl.classList.add('form-control-sm');
				if (label !== 'none')
					labelEl.classList.add('small'); // Bootstrap의 작은 텍스트 클래스
				break;
			case 'l':
				inputEl.classList.add('form-control-lg');
				if (label !== 'none')
					labelEl.classList.add('fs-1'); // Bootstrap의 큰 텍스트 클래스
				break;
			case 'xl':
				inputEl.classList.add('form-control-xl');
				if (label !== 'none')
					labelEl.classList.add('fs-0')
			default:
				if (label !== 'none')
					labelEl.classList.add('fs-6'); // 중간 크기 텍스트를 위한 Bootstrap 클래스
		}

		// 변경: 입력 필드를 감싸는 div 추가
		const inputWrapper = document.createElement('div');
		inputWrapper.classList.add('col-sm-9');
		inputWrapper.appendChild(inputEl);
		this.el.appendChild(inputWrapper);

		this.render();
	}

	getValue() {
		return this.el.querySelector('input').value.trim();
	}

	setValue(value) {
		this.el.querySelector('input').value = value;
	}

	render() {
		// 추가적인 렌더링 로직이 필요할 경우 여기에 작성
	}
}