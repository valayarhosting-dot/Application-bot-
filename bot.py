import discord
from discord.ext import commands

TOKEN = "YOUR_BOT_TOKEN"
GUILD_ID = 1417908779890114733          # Your server ID
STAFF_CHANNEL_ID = 1419258212191961128  # Staff review channel
FACTION_CHANNEL_ID = 1417992968794669130 # Faction application channel
ROLE_WHITELIST_ID = 1418220278785245205 # Whitelisted role
PUBLIC_NOTIFY_CHANNEL_ID = 1418591686329630761  # Public whitelist notifications

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


# Buttons for Faction/Whitelist Review
class ApplicationView(discord.ui.View):
    def __init__(self, applicant_id):
        super().__init__(timeout=None)
        self.applicant_id = applicant_id

    @discord.ui.button(label="✅ Accept", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        member = guild.get_member(self.applicant_id)

        if member:
            role = guild.get_role(ROLE_WHITELIST_ID)
            if role:
                await member.add_roles(role)

            # DM confirmation
            try:
                await member.send("🎉 Congratulations! Your application was **accepted** and you are now whitelisted.")
            except:
                pass

            # Public notification
            public_channel = guild.get_channel(PUBLIC_NOTIFY_CHANNEL_ID)
            if public_channel:
                await public_channel.send(f"🎉 {member.mention} has been **whitelisted** for Norex City Roleplay!")

            await interaction.response.send_message(f"✅ Accepted {member.mention}", ephemeral=True)
        else:
            await interaction.response.send_message("⚠️ Member not found.", ephemeral=True)
        self.stop()

    @discord.ui.button(label="❌ Deny", style=discord.ButtonStyle.red)
    async def deny(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.guild.get_member(self.applicant_id)
        if member:
            try:
                await member.send("❌ Sorry, your application was **denied**.")
            except:
                pass
        await interaction.response.send_message("🚫 Application denied.", ephemeral=True)
        self.stop()


# Bot Ready
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"🔗 Synced {len(synced)} commands")
    except Exception as e:
        print(f"❌ Error syncing: {e}")


# /help command
@bot.tree.command(name="help", description="Show available application commands")
async def help_cmd(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📖 Help Menu",
        description="Here are the available application commands:",
        color=discord.Color.green()
    )
    embed.add_field(name="/apply staff", value="Apply to become a staff member.", inline=False)
    embed.add_field(name="/apply whitelist", value="Apply to get whitelisted for Norex City RP.", inline=False)
    embed.add_field(name="/apply faction", value="Apply for factions (PD, News, EMS, Mechanic).", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)


# /apply base
@bot.tree.command(name="apply", description="Application commands for staff, whitelist, and factions")
async def apply(interaction: discord.Interaction):
    await interaction.response.send_message("⚠️ Please choose `/apply staff`, `/apply whitelist`, or `/apply faction`.", ephemeral=True)


# Staff Application
@bot.tree.command(name="apply_staff", description="Apply for staff in Norex City RP")
async def apply_staff(interaction: discord.Interaction):
    await interaction.response.send_message("📋 Starting your **staff application** in DMs...", ephemeral=True)
    try:
        await interaction.user.send("👋 Hello! Let’s begin your **staff application** for Norex City RP.\n\n")

        questions = [
            "1️⃣ What is your real name?",
            "2️⃣ How old are you?",
            "3️⃣ Why do you want to become staff?",
            "4️⃣ Do you have any past staff experience?",
            "5️⃣ How many hours can you dedicate daily?",
        ]
        answers = []
        for q in questions:
            await interaction.user.send(q)
            def check(msg): return msg.author == interaction.user and isinstance(msg.channel, discord.DMChannel)
            msg = await bot.wait_for("message", check=check)
            answers.append(msg.content)

        staff_channel = bot.get_channel(STAFF_CHANNEL_ID)
        if staff_channel:
            embed = discord.Embed(title="📥 New Staff Application", color=discord.Color.blue())
            embed.set_author(name=interaction.user, icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
            for i, q in enumerate(questions):
                embed.add_field(name=q, value=answers[i], inline=False)
            await staff_channel.send(embed=embed)

        await interaction.user.send("✅ Your staff application has been submitted!")
    except discord.Forbidden:
        await interaction.followup.send("⚠️ I couldn’t DM you! Please enable DMs.", ephemeral=True)


# Whitelist Application
@bot.tree.command(name="apply_whitelist", description="Apply for whitelist in Norex City RP")
async def apply_whitelist(interaction: discord.Interaction):
    await interaction.response.send_message("📋 Starting your **whitelist application** in DMs...", ephemeral=True)
    try:
        await interaction.user.send("👋 Hello! Let’s begin your **whitelist application** for Norex City RP.\n\n")

        questions = [
            "1️⃣ What is your in-game name (SA-MP)?",
            "2️⃣ What is your Discord username?",
            "3️⃣ How old are you?",
            "4️⃣ Why do you want to join Norex City Roleplay?",
            "5️⃣ Do you have any past RP experience?",
            "6️⃣ How many hours can you play daily?",
        ]
        answers = []
        for q in questions:
            await interaction.user.send(q)
            def check(msg): return msg.author == interaction.user and isinstance(msg.channel, discord.DMChannel)
            msg = await bot.wait_for("message", check=check)
            answers.append(msg.content)

        staff_channel = bot.get_channel(STAFF_CHANNEL_ID)
        if staff_channel:
            embed = discord.Embed(title="📥 New Whitelist Application", color=discord.Color.purple())
            embed.set_author(name=interaction.user, icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
            for i, q in enumerate(questions):
                embed.add_field(name=q, value=answers[i], inline=False)
            view = ApplicationView(interaction.user.id)
            await staff_channel.send(embed=embed, view=view)

        await interaction.user.send("✅ Your whitelist application has been submitted!")
    except discord.Forbidden:
        await interaction.followup.send("⚠️ I couldn’t DM you! Please enable DMs.", ephemeral=True)


# Faction Application
@bot.tree.command(name="apply_faction", description="Apply for factions in Norex City RP")
async def apply_faction(interaction: discord.Interaction, faction: str):
    await interaction.response.send_message(f"📋 Starting your **{faction} application** in DMs...", ephemeral=True)
    try:
        await interaction.user.send(f"👋 Hello! Let’s begin your **{faction} application** for Norex City RP.\n\n")

        questions = [
            f"1️⃣ Why do you want to join {faction}?",
            f"2️⃣ Do you have past experience in {faction} roleplay?",
            "3️⃣ How active can you be daily?",
            "4️⃣ What skills do you bring to the faction?",
        ]
        answers = []
        for q in questions:
            await interaction.user.send(q)
            def check(msg): return msg.author == interaction.user and isinstance(msg.channel, discord.DMChannel)
            msg = await bot.wait_for("message", check=check)
            answers.append(msg.content)

        faction_channel = bot.get_channel(FACTION_CHANNEL_ID)
        if faction_channel:
            embed = discord.Embed(title=f"📥 New {faction} Application", color=discord.Color.orange())
            embed.set_author(name=interaction.user, icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
            for i, q in enumerate(questions):
                embed.add_field(name=q, value=answers[i], inline=False)
            await faction_channel.send(embed=embed)

        await interaction.user.send(f"✅ Your {faction} application has been submitted!")
    except discord.Forbidden:
        await interaction.followup.send("⚠️ I couldn’t DM you! Please enable DMs.", ephemeral=True)


bot.run(TOKEN)