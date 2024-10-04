import { Component } from "../../core/core.js";
import { ProfileLevel } from "./ProfileLevel.js";
import { Button } from "../Button.js";
import { getCookie, selectProfileImg } from "../../core/core.js";
import { Input } from "../Input.js";

export class ProfileSummary extends Component {
	constructor(props) {
		super({
			props: {
				className: 'profile-summary',
			}
		});
		this.profileContentsRender(props);
	}

	profileContentsRender(props) {
		const username = getCookie('player');
		this.el.innerHTML = /*html*/`
			<div class="profile-summary-img-level">
				<div class="profile-summary-img"></div>
			</div>
			<div class="profile-summary-name">
				<div>${username}</div>
			</div>
			<div class="vertical-line"></div>
			<div class="profile-summary-win">
				<p>승부 요약</p>
				<span>${props.win_cnt}승 ${props.lose_cnt}패</span>
			</div>
			<div class="vertical-line"></div>
			<div class="button-container"></div>
		`;

		//프로필 이미지
		const profileImg = this.el.querySelector('.profile-summary-img');
		const img = document.createElement('img');
		img.src = selectProfileImg(props.profile_img);
		profileImg.appendChild(img);

		//유저 이름 & 프로필 레벨
		const profileImgLevel = this.el.querySelector('.profile-summary-img-level');
		profileImgLevel.appendChild(new ProfileLevel(props.exp).el);

		const profileName = this.el.querySelector('.profile-summary-name');

		profileName.appendChild(new Input(
			'', 'text', {
			background: "url('../../../public/images/ui/profile-input.png')",
			width: '300px',
			height: '50px',
			fontsize: '20px',
		}, props.status_msg).el);

		// 승부 요약
		const profileWin = this.el.querySelector('.profile-summary-win');

		const logoutBtn = new Button({
			width: '130px',
			height: '60px',
			size: '25px',
			background: "url('../../../public/images/ui/profile-button.png')",
		},
			'로그아웃',
			async () => {
				const response = await fetch('/api/users/logout/', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						'X-CSRF-Token': getCookie('csrftoken'),
					},
				});
				const status = await response.status;
				if (status === 200) {
					document.cookie = 'ppstate=; player=;';
					location.href = '/#/';
					alert('로그아웃 되었습니다.');
				}
				else
					alert('로그아웃에 실패했습니다.');
			}
		);
		const withdrawalBtn = new Button({
			width: '130px',
			height: '60px',
			size: '25px',
			background: "url('../../../public/images/ui/profile-button.png')",
		},
			'회원탈퇴',
			() => {
				// 회원 탈퇴 로직
			});

		const saveBtn = new Button({
			width: '200px',
			height: '100px',
			size: '25px',
			background: "url('../../../public/images/ui/profile-button.png')",
		},
			'저장하기',
			() => {
				// 저장하기 로직
			});
		this.el.querySelector('.button-container').appendChild(logoutBtn.el);
		this.el.querySelector('.button-container').appendChild(withdrawalBtn.el);
		this.el.appendChild(saveBtn.el);
	}
}