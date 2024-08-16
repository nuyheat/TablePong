# Generated by Django 5.0.7 on 2024-08-10 07:59

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('match_id', models.AutoField(primary_key=True, serialize=False)),
                ('match_result', models.CharField(blank=True, choices=[('user_win', '사용자 승리'), ('opponent_win', '상대방 승리'), ('pending_result', '결과 대기중')], default='pending_result', max_length=40)),
                ('match_start_time', models.DateTimeField(auto_now_add=True)),
                ('match_end_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('match_user_grade', models.IntegerField(blank=True, default=0)),
                ('match_rival_grade', models.IntegerField(blank=True, default=0)),
                ('match_type', models.CharField(choices=[('tournament', '토너먼트 경기'), ('match', '1대1경기')], default='match', max_length=10)),
                ('rival_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rival_id', to='users.user')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_id', to='users.user')),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('tournament_id', models.AutoField(primary_key=True, serialize=False)),
                ('bonus_match_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bonus_match_id', to='games.match')),
                ('final_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='final_id', to='games.match')),
                ('semifinal_id1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='semifinal_id1', to='games.match')),
                ('semifinal_id2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='semifinal_id2', to='games.match')),
            ],
        ),
    ]
